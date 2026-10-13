// Export texture experiment variants from one hierarchy, isolating baking variance.
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
    nx::ExportNxs reconstruction, reconstructionFine, divisor1, divisor2;
    const auto prefix = std::filesystem::path(params.output.toStdString()).replace_extension().string();
    reconstruction.export_nxs(hierarchy, prefix + ".reconstruction.nxs", 0, false, params.texture_error_divisor);
    reconstructionFine.export_nxs(hierarchy, prefix + ".reconstructionFine.nxs", params.texture_error_ratio, false, params.texture_error_divisor);
    divisor1.export_nxs(hierarchy, prefix + ".divisor1.nxs", params.texture_error_ratio, false, 1);
    divisor2.export_nxs(hierarchy, prefix + ".divisor2.nxs", params.texture_error_ratio, false, 2);
    std::cout << "Exported " << prefix << ".{reconstruction,reconstructionFine,divisor1,divisor2}.nxs from one hierarchy\n";
  } catch (const std::exception &error) { std::cerr << error.what() << '\n'; return 1; }
}
