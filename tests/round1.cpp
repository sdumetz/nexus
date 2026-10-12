#include "../src/texture/texel_error.h"
#include "../src/core/mesh_hierarchy.h"
#include "../src/nxsbuild/export_nxs.h"
#include <fstream>
#include <iostream>
#include <stdexcept>

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
		node.error = !coarse && i == 0 ? 0.1f : 0.001f;
	}
	if(textured) {
		mesh->allocate_node_textures_and_texels(256, 3);
		std::fill(mesh->texels.data(), mesh->texels.data() + mesh->texels.size(), 127);
	}
	return mesh;
}

static void export_checks(bool textured) {
	nx::MeshHierarchy hierarchy;
	hierarchy.levels = {level(textured, false), level(textured, true)};
	nx::ExportNxs exporter;
	const std::string name = textured ? "textured.nxs" : "geometry.nxs";
	exporter.export_nxs(hierarchy, name);
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

int main() {
	metric_checks();
	export_checks(true);
	export_checks(false);
	std::cout << "Round 1 checks passed\n";
}
