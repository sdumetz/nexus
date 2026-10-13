#include "../src/texture/texel_error.h"
#include "../src/texture/texture_sizing.h"
#include "../src/texture/texture_loss.h"
#include "../src/core/mesh_hierarchy.h"
#include "../src/nxsbuild/export_nxs.h"
#include "../src/nxsbuild/build_parameters.h"
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <cstring>
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
	near(nodes[2].error, 0.001f); // Low reconstruction loss leaves geometry dominant.
	near(nodes[3].error, 0);      // Sink remains zero.
	std::cout << name << ": geometry/texture maximum and ancestor saturation passed\n";
}

static void sizing_checks(bool halving) {
	nx::MeshHierarchy hierarchy;
	hierarchy.levels = {level(true, false), level(true, true)};
	std::vector<std::vector<char>> baseline_geometry;
	for(float ratio: {0.0f, 1.0f, 0.5f}) {
		nx::ExportNxs exporter;
		// Exercise the API default as well as explicitly configured ratios.
		exporter.export_nxs(hierarchy, "sizing.nxs", ratio, halving);
		std::ifstream file("sizing.nxs", std::ios::binary);
		nx::Header header;
		file.read(reinterpret_cast<char*>(&header), sizeof(header));
		std::vector<nx::Node> nodes(header.n_nodes);
		file.read(reinterpret_cast<char*>(nodes.data()), nodes.size()*sizeof(nx::Node));
		if(header.version != 2 || header.n_nodes != 4 || header.n_textures != 4)
			throw std::runtime_error("Sizing changed container layout");
		near(nodes[0].error, 0.101f);
		near(nodes[1].error, 0.1f);
		near(nodes[2].error, 0.001f);
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
			const int expected = i == 2 || ratio == 0 ? 256 : (halving ? (ratio == 1 ? 32 : 64) : (ratio == 1 ? 20 : 40));
			if(image.width() != expected || image.height() != expected)
				throw std::runtime_error("Unexpected texture dimensions");
			if(i < 2 && ratio > 0) {
				// This resolution meets the target, but one step coarser would not.
				const float target = ratio*(i == 0 ? 0.101f : 0.1f);
				if(2.0f/expected > target || 2.0f/(halving ? expected/2 : expected-4) <= target)
					throw std::runtime_error("Texture was not sized to the coarsest allowed resolution");
			}
			const auto top = image.pixelColor(0,0), bottom = image.pixelColor(expected-1,expected-1);
			// Small non-power-of-two JPEGs have stronger endpoint ringing.
			if(top.red() > 24 || top.green() < 230 || bottom.red() < 230 || bottom.green() > 24)
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

static void loss_checks() {
	QImage source(16,16,QImage::Format_RGB32), decoded(16,16,QImage::Format_RGB32), mask(16,16,QImage::Format_RGB32);
	source.fill(qRgb(128,128,128)); decoded.fill(qRgb(120,120,120)); mask.fill(Qt::white);
	auto loss = nx::texture_reconstruction_loss(source,decoded,mask,2);
	near(loss.rms,8); near(loss.error,1);
	near(nx::texture_reconstruction_loss(source,decoded,mask,2,1).error,2);
	near(nx::texture_reconstruction_loss(source,decoded,mask,2,4).error,0.5f);
	decoded.fill(qRgb(124,124,124));
	loss = nx::texture_reconstruction_loss(source,decoded,mask,2);
	near(loss.rms,4); near(loss.error,0.5f);
	near(nx::texture_reconstruction_loss(source,source,mask,2).error,0);
	decoded.fill(qRgb(0,0,0));
	near(nx::texture_reconstruction_loss(source,decoded,mask,2).error,1);
	// Only one occupied pixel: arbitrary differences in atlas padding are ignored.
	mask.fill(Qt::black); mask.setPixel(3,7,qRgb(255,255,255)); decoded.setPixel(3,7,source.pixel(3,7));
	loss = nx::texture_reconstruction_loss(source,decoded,mask,2);
	if(loss.pixels != 1) throw std::runtime_error("Incorrect occupied-pixel count");
	near(loss.error,0);
	mask.fill(Qt::black);
	near(nx::texture_reconstruction_loss(source,decoded,mask,2).error,1);
	QImage small(4,4,QImage::Format_RGB32); small.fill(qRgb(128,128,128)); mask.fill(Qt::white);
	near(nx::texture_reconstruction_loss(source,small,mask,2).error,0);
	for(double divisor: {0.0,-1.0,std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()}) {
		bool rejected = false;
		try { nx::texture_reconstruction_loss(source,decoded,mask,2,divisor); }
		catch(const std::invalid_argument &) { rejected = true; }
		if(!rejected) throw std::runtime_error("Invalid texture error divisor accepted");
	}
	// Real exporter: division by two halves the texture contribution, including
	// ancestor saturation, while preserving all geometry and JPEG bytes.
	nx::MeshHierarchy hierarchy;
	hierarchy.levels = {level(true,false),level(true,true)};
	for(auto *mesh: hierarchy.levels)
		for(auto &node: mesh->micronodes) node.error = 0;
	for(float ratio: {0.0f,1.0f}) {
		nx::ExportNxs footprint, reconstruction;
		footprint.export_nxs(hierarchy,"loss-footprint.nxs",ratio,false,1);
		reconstruction.export_nxs(hierarchy,"loss-reconstruction.nxs",ratio); // Default divisor 2.
		std::ifstream a("loss-footprint.nxs",std::ios::binary), b("loss-reconstruction.nxs",std::ios::binary);
		nx::Header headerA,headerB;
		a.read(reinterpret_cast<char*>(&headerA),sizeof(headerA)); b.read(reinterpret_cast<char*>(&headerB),sizeof(headerB));
		if(std::memcmp(&headerA,&headerB,sizeof(headerA))) throw std::runtime_error("Metric changed header");
		std::vector<nx::Node> na(headerA.n_nodes),nb(headerB.n_nodes);
		a.read(reinterpret_cast<char*>(na.data()),na.size()*sizeof(nx::Node));
		b.read(reinterpret_cast<char*>(nb.data()),nb.size()*sizeof(nx::Node));
		if(nb[0].error < nb[1].error || nb[0].error < nb[2].error || nb.back().error != 0)
			throw std::runtime_error("Reconstruction metric broke ancestor monotonicity or sink");
		bool reduced = false;
		for(size_t i=0;i<na.size();++i) {
			near(nb[i].error,na[i].error/2);
			reduced |= nb[i].error < na[i].error;
			nb[i].error = na[i].error;
			if(std::memcmp(&na[i],&nb[i],sizeof(nx::Node))) throw std::runtime_error("Metric changed node geometry metadata");
		}
		if(!reduced) throw std::runtime_error("Default divisor had no effect");
		const std::vector<char> restA((std::istreambuf_iterator<char>(a)),{}), restB((std::istreambuf_iterator<char>(b)),{});
		if(restA != restB) throw std::runtime_error("Metric changed geometry, patches or texture bytes");
	}
	std::cout << "Reconstruction loss, occupied pixels, calibration, fallback and binary export passed\n";
}

static void parameter_checks() {
	auto parse = [](std::vector<std::string> args, nx::BuildParameters &parameters) {
		std::vector<char*> argv;
		for(auto &arg: args) argv.push_back(arg.data());
		return parameters.parse(argv.size(),argv.data());
	};
	nx::BuildParameters defaults;
	if(!parse({"nxsbuild","model.obj"},defaults)) throw std::runtime_error("Default arguments rejected");
	near(defaults.texture_error_divisor,2);
	for(const auto &value: {"0.5","1","4"}) {
		nx::BuildParameters parameters;
		if(!parse({"nxsbuild","--texture-error-divisor",value,"model.obj"},parameters))
			throw std::runtime_error("Valid texture error divisor rejected");
		near(parameters.texture_error_divisor,std::stof(value));
	}
	for(const auto &value: {"0","-1","nan","inf","not-a-number"}) {
		nx::BuildParameters parameters;
		if(parse({"nxsbuild","--texture-error-divisor",value,"model.obj"},parameters))
			throw std::runtime_error("Invalid texture error divisor accepted by CLI");
	}
	nx::BuildParameters obsolete;
	if(parse({"nxsbuild","--texture-error-metric","footprint","model.obj"},obsolete))
		throw std::runtime_error("Removed texture metric opt-out accepted");
	std::cout << "Default divisor, tuning arguments, validation and removed opt-out passed\n";
}

int main() {
	for(const auto dims: {std::make_pair(256,256), std::make_pair(256,128)}) {
		auto footprint = [](int w, int h) { return std::max(2.0/w, 1.0/h); };
		const auto size = nx::fine_texture_size(dims.first, dims.second, 0.1, footprint);
		if(size != (dims.first == dims.second ? std::make_pair(20,20) : std::make_pair(20,12)))
			throw std::runtime_error("Fine sizing failed square/rectangular rounding");
		if(footprint(size.first,size.second) > 0.1 || footprint(size.first-4,size.second) <= 0.1)
			throw std::runtime_error("Fine sizing failed target/minimality check");
		if(nx::fine_texture_size(dims.first,dims.second,0,footprint) != dims ||
		   nx::fine_texture_size(dims.first,dims.second,1e-8,footprint) != dims ||
		   nx::fine_texture_size(dims.first,dims.second,1e6,footprint) != std::make_pair(4,4))
			throw std::runtime_error("Fine sizing failed bounds");
	}
	metric_checks();
	export_checks(true);
	export_checks(false);
	export_checks(false, 1);
	sizing_checks(true);
	sizing_checks(false);
	loss_checks();
	parameter_checks();
	std::cout << "Texture rounds 1-4 checks passed\n";
}
