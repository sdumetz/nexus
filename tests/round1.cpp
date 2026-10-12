#include "../src/texture/texel_error.h"
#include "../src/core/mesh_hierarchy.h"
#include "../src/nxsbuild/export_nxs.h"
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <QImage>

static void near(float actual, float expected) {
	if(!std::isfinite(actual) || std::abs(actual - expected) > 1e-6f)
		throw std::runtime_error("Expected " + std::to_string(expected) + ", got " + std::to_string(actual));
}

static void metric_checks() {
	nx::Vector3f p[3] = {{0,0,0}, {2,0,0}, {0,2,0}};
	nx::Vector2f uv[3] = {{0,0}, {1,0}, {0,1}};
	near(nx::triangle_texel_error(p, uv, 256, 256), 2.0f/256);
	near(nx::triangle_texel_error(p, uv, 128, 128), 2.0f/128);
	near(nx::triangle_texel_error(p, uv, 256, 128), 2.0f/128);
	uv[1].u = 0.5f;
	near(nx::triangle_texel_error(p, uv, 256, 256), 4.0f/256);
	// Rotate the image chart: the footprint must not depend on UV orientation.
	const float s = std::sqrt(0.5f);
	uv[0] = {0.5f,0}; uv[1] = {0.5f+s,s}; uv[2] = {0.5f-s,s};
	near(nx::triangle_texel_error(p, uv, 256, 256), 2.0f/256);
	// Collapsed/subpixel charts have a finite whole-triangle fallback.
	uv[0] = uv[1] = uv[2] = {0,0};
	near(nx::triangle_texel_error(p, uv, 256, 256), std::sqrt(8.0f));
	uv[1] = {1e-12f,0}; uv[2] = {0,1e-12f};
	near(nx::triangle_texel_error(p, uv, 256, 256), std::sqrt(8.0f));
	p[1] = p[2] = p[0];
	near(nx::triangle_texel_error(p, uv, 256, 256), 0);
	near(nx::MicroNode{}.error, 0);
}

static nx::MappedMesh* level(bool textured, bool coarse) {
	auto* mesh = new nx::MappedMesh;
	mesh->has_textures = textured;
	mesh->has_normals = true;
	mesh->positions.resize(3);
	mesh->positions[0] = {0,0,0}; mesh->positions[1] = {2,0,0}; mesh->positions[2] = {0,2,0};
	mesh->normals.resize(3);
	mesh->texcoords.resize(3);
	mesh->texcoords[0] = {0,0}; mesh->texcoords[1] = {1,0}; mesh->texcoords[2] = {0,1};
	mesh->wedges.resize(3);
	for(nx::Index i = 0; i < 3; ++i) {
		mesh->normals[i] = {0,0,1};
		mesh->wedges[i] = {i,i,i};
	}
	mesh->triangles.resize(2);
	mesh->clusters.resize(2);
	for(nx::Index i = 0; i < 2; ++i) {
		mesh->triangles[i] = {{0,1,2}};
		mesh->clusters[i] = {i,1,{0,0,0},3,coarse ? i : nx::NONE};
	}
	mesh->micronodes.resize(coarse ? 1 : 2);
	for(nx::Index i = 0; i < mesh->micronodes.size(); ++i) {
		auto &node = mesh->micronodes[i];
		node.id = i;
		node.cluster_ids = coarse ? std::vector<nx::Index>{0,1} : std::vector<nx::Index>{i};
		node.center = {0,0,0}; node.radius = 3;
		node.error = coarse ? 0.0f : (i == 0 ? 0.1f : 0.001f);
	}
	if(textured) {
		mesh->allocate_node_textures_and_texels(256, 3);
		for(const nx::NodeTexture &texture: mesh->node_textures) {
			for(int y = 0; y < 256; ++y) for(int x = 0; x < 256; ++x) {
				auto *pixel = mesh->texels.data() + texture.offset + (y*256+x)*3;
				pixel[0] = x; pixel[1] = y; pixel[2] = 128;
			}
		}
	}
	return mesh;
}

static void export_checks(bool textured, float ratio = 0) {
	nx::MeshHierarchy hierarchy;
	hierarchy.levels = {level(textured, false), level(textured, true)};
	nx::ExportNxs exporter;
	const std::string name = textured ? "textured.nxs" : "geometry.nxs";
	exporter.export_nxs(hierarchy, name, ratio);
	std::ifstream file(name, std::ios::binary);
	nx::Header header;
	file.read(reinterpret_cast<char*>(&header), sizeof(header));
	if(header.magic != 0x4E787320 || header.version != 2 || header.n_nodes != 4
		|| header.n_textures != (textured ? 4u : 0u))
		throw std::runtime_error("Unexpected container layout");
	nx::Node nodes[4];
	file.read(reinterpret_cast<char*>(nodes), sizeof(nodes));
	if(!file) throw std::runtime_error("Truncated nodes");
	near(nodes[0].error, 0.101f); // Saturated above its geometry-dominated child.
	near(nodes[1].error, 0.1f);   // Geometry dominates.
	near(nodes[2].error, textured ? 2.0f/256 : 0.001f); // Texture dominates, or absent.
	near(nodes[3].error, 0);      // Sink remains zero.
	std::cout << name << ": geometry/texture maximum and ancestor saturation passed\n";
}

static void sizing_checks() {
	nx::MeshHierarchy hierarchy;
	hierarchy.levels = {level(true, false), level(true, true)};
	std::vector<std::vector<char>> baseline_geometry;
	for(float ratio: {0.0f, 1.0f, 0.5f}) {
		nx::ExportNxs exporter;
		// Exercise the API default as well as explicitly configured ratios.
		if(ratio == 1) exporter.export_nxs(hierarchy, "sizing.nxs");
		else exporter.export_nxs(hierarchy, "sizing.nxs", ratio);
		std::ifstream file("sizing.nxs", std::ios::binary);
		nx::Header header;
		file.read(reinterpret_cast<char*>(&header), sizeof(header));
		std::vector<nx::Node> nodes(header.n_nodes);
		file.read(reinterpret_cast<char*>(nodes.data()), nodes.size()*sizeof(nx::Node));
		if(header.version != 2 || header.n_nodes != 4 || header.n_textures != 4)
			throw std::runtime_error("Sizing changed container layout");
		near(nodes[0].error, 0.101f);
		near(nodes[1].error, 0.1f);
		near(nodes[2].error, 2.0f/256);
		near(nodes[3].error, 0);
		std::vector<nx::Texture> textures(header.n_textures);
		file.seekg(sizeof(nx::Header) + nodes.size()*sizeof(nx::Node) + header.n_patches*sizeof(nx::Patch));
		file.read(reinterpret_cast<char*>(textures.data()), textures.size()*sizeof(nx::Texture));
		for(size_t i = 0; i < 3; ++i) {
			std::vector<char> blob(textures[i].getSize());
			file.seekg(textures[i].getBeginOffset());
			file.read(blob.data(), blob.size());
			QImage image;
			if(!image.loadFromData(reinterpret_cast<const uchar*>(blob.data()), blob.size(), "JPEG"))
				throw std::runtime_error("Exported texture cannot be decoded");
			const int expected = i == 2 || ratio == 0 ? 256 : (ratio == 1 ? 32 : 64);
			if(image.width() != expected || image.height() != expected)
				throw std::runtime_error("Unexpected texture dimensions");
			if(i < 2 && ratio > 0) {
				// This resolution meets the target, but one step coarser would not.
				const float target = ratio*(i == 0 ? 0.101f : 0.1f);
				if(2.0f/expected > target || 4.0f/expected <= target)
					throw std::runtime_error("Texture was not sized to the coarsest allowed resolution");
			}
			const auto top = image.pixelColor(0,0), bottom = image.pixelColor(expected-1,expected-1);
			if(top.red() > 12 || top.green() < 240 || bottom.red() < 240 || bottom.green() > 12)
				throw std::runtime_error("Downsampled texture gradient/orientation changed");
			const size_t geometry_size = nodes[i].nvert*header.signature.vertex.size()
				+ nodes[i].nface*header.signature.face.size();
			std::vector<char> geometry(geometry_size);
			file.seekg(nodes[i].getBeginOffset());
			file.read(geometry.data(), geometry.size());
			if(!file) throw std::runtime_error("Truncated export");
			if(ratio == 0) baseline_geometry.push_back(geometry);
			else if(geometry != baseline_geometry[i])
				throw std::runtime_error("Sizing changed geometry/UV payloads");
		}
		for(const auto *mesh: hierarchy.levels) {
			for(const nx::NodeTexture &texture: mesh->node_textures)
				if(texture.width != 256 || texture.height != 256)
					throw std::runtime_error("Sizing modified baked textures");
		}
	}
	// Without a positive geometric target, preserve baked detail.
	for(auto *mesh: hierarchy.levels)
		for(auto &node: mesh->micronodes) node.error = 0;
	nx::ExportNxs exporter;
	exporter.export_nxs(hierarchy, "zero-target.nxs");
	std::ifstream file("zero-target.nxs", std::ios::binary);
	nx::Header header;
	file.read(reinterpret_cast<char*>(&header), sizeof(header));
	file.seekg(sizeof(nx::Header) + header.n_nodes*sizeof(nx::Node) + header.n_patches*sizeof(nx::Patch));
	std::vector<nx::Texture> textures(header.n_textures);
	file.read(reinterpret_cast<char*>(textures.data()), textures.size()*sizeof(nx::Texture));
	for(size_t i = 0; i + 1 < textures.size(); ++i) {
		std::vector<char> blob(textures[i].getSize());
		file.seekg(textures[i].getBeginOffset());
		file.read(blob.data(), blob.size());
		QImage image;
		if(!image.loadFromData(reinterpret_cast<const uchar*>(blob.data()), blob.size(), "JPEG")
			|| image.width() != 256 || image.height() != 256)
			throw std::runtime_error("Zero geometric target lost texture detail");
	}
	std::cout << "Round 2 sizing, zero-error root, JPEG decode, and geometry preservation passed\n";
}

int main() {
	metric_checks();
	export_checks(true);
	export_checks(false);
	export_checks(false, 1);
	sizing_checks();
	std::cout << "Round 1 and round 2 checks passed\n";
}
