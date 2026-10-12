#ifndef NX_TEXEL_ERROR_H
#define NX_TEXEL_ERROR_H

#include "../core/mesh_types.h"
#include <algorithm>
#include <cmath>
#include <limits>

namespace nx {

// Largest world-space footprint of a pixel on a UV-mapped triangle. Use the
// largest singular value of the pixel-to-world Jacobian, so anisotropic charts
// and rectangular images are handled independently of their orientation.
inline float triangle_texel_error(const Vector3f (&p)[3], const Vector2f (&uv)[3],
		int width, int height) {
	if(width <= 0 || height <= 0)
		return 0.0f;

	double e[2][3] = {
		{double(p[1].x) - p[0].x, double(p[1].y) - p[0].y, double(p[1].z) - p[0].z},
		{double(p[2].x) - p[0].x, double(p[2].y) - p[0].y, double(p[2].z) - p[0].z}
	};
	double diameter2 = 0;
	for(int i = 0; i < 3; ++i) {
		double edge2 = 0;
		for(int k = 0; k < 3; ++k) {
			const double d = i < 2 ? e[i][k] : e[1][k] - e[0][k];
			edge2 += d*d;
		}
		diameter2 = std::max(diameter2, edge2);
	}

	const double a = (double(uv[1].u) - uv[0].u)*width;
	const double b = (double(uv[1].v) - uv[0].v)*height;
	const double c = (double(uv[2].u) - uv[0].u)*width;
	const double d = (double(uv[2].v) - uv[0].v)*height;
	const double det = a*d - b*c;
	const double scale = std::hypot(a, b)*std::hypot(c, d);
	// A collapsed UV chart has no invertible density. Its entire triangle can
	// occupy one pixel; use its diameter rather than returning zero or NaN.
	if(std::abs(det) <= std::numeric_limits<double>::epsilon()*scale)
		return static_cast<float>(std::sqrt(diameter2));

	double xx = 0, xy = 0, yy = 0;
	for(int k = 0; k < 3; ++k) {
		const double x = (d*e[0][k] - b*e[1][k])/det;
		const double y = (a*e[1][k] - c*e[0][k])/det;
		xx += x*x;
		xy += x*y;
		yy += y*y;
	}
	const double eigenvalue = 0.5*(xx + yy + std::hypot(xx - yy, 2*xy));
	// A footprint cannot cover more than this finite triangle. This also bounds
	// extremely thin/subpixel UV charts without hiding them as zero-density.
	return static_cast<float>(std::sqrt(std::min(eigenvalue, diameter2)));
}

} // namespace nx
#endif
