// Export both rounds from one hierarchy, isolating sizing from baking variance.
#include "../../src/nxsbuild/build_parameters.h"
#include "../../src/nxsbuild/export_nxs.h"
#include "../../src/core/mesh_hierarchy.h"
#include "../../src/loaders/meshloader.h"
#include <QCoreApplication>
#include <QLocale>
#include <filesystem>
#include <iostream>

int main(int argc, char **argv) {
  QCoreApplication app(argc, argv);
  QLocale::setDefault(QLocale::C);
  nx::BuildParameters params;
  if (!params.parse(argc, argv) || params.inputs.size() != 1 || params.resume) return 1;
  nx::setVerbosity(params.verbosity);
  try {
    nx::MeshHierarchy hierarchy;
    auto *mesh = new nx::MappedMesh;
    std::vector<nx::Material> materials;
    nx::load_mesh(std::filesystem::path(params.inputs.first().toStdString()), *mesh, materials);
    hierarchy.initialize(mesh, materials);
    hierarchy.build_hierarchy(params);
    nx::ExportNxs round1, round2, fine;
    const auto prefix = std::filesystem::path(params.output.toStdString()).replace_extension().string();
    round1.export_nxs(hierarchy, prefix + ".round1.nxs", 0);
    round2.export_nxs(hierarchy, prefix + ".round2.nxs", params.texture_error_ratio, true);
    fine.export_nxs(hierarchy, prefix + ".fine.nxs", params.texture_error_ratio);
    std::cout << "Exported " << prefix << ".round{1,2}.nxs from one hierarchy\n";
  } catch (const std::exception &error) { std::cerr << error.what() << '\n'; return 1; }
}
