#ifndef NX_TEXTURE_LOSS_H
#define NX_TEXTURE_LOSS_H

#include <QImage>
#include <algorithm>
#include <cmath>
#include <stdexcept>

namespace nx {
struct TextureLoss {
	double rms = 0; // RGB code values, 0..255; not a perceptual color distance.
	size_t pixels = 0;
	float error = 0;
};

// Experimental conversion of reconstruction loss to a world-space refinement
// heuristic. The calibration is explicit: an RMS of 8 restores the original
// footprint; smaller losses reduce it. This is not a surface-deviation bound.
inline TextureLoss texture_reconstruction_loss(const QImage &reference, const QImage &decoded,
		const QImage &occupied, float footprint, double calibration = 8.0) {
	if(reference.isNull() || decoded.isNull() || occupied.size() != reference.size() ||
	   !std::isfinite(calibration) || calibration <= 0)
		throw std::invalid_argument("Invalid texture reconstruction inputs");
	const QImage original = reference.convertToFormat(QImage::Format_RGB32);
	const QImage reconstructed = decoded.scaled(reference.size(), Qt::IgnoreAspectRatio,
		Qt::SmoothTransformation).convertToFormat(QImage::Format_RGB32);
	const QImage mask = occupied.convertToFormat(QImage::Format_RGB32);
	TextureLoss loss;
	double squared = 0;
	for(int y = 0; y < original.height(); ++y) {
		const auto *a = reinterpret_cast<const QRgb*>(original.constScanLine(y));
		const auto *b = reinterpret_cast<const QRgb*>(reconstructed.constScanLine(y));
		const auto *m = reinterpret_cast<const QRgb*>(mask.constScanLine(y));
		for(int x = 0; x < original.width(); ++x) {
			if(qRed(m[x]) == 0) continue;
			const double r = qRed(a[x])-qRed(b[x]);
			const double g = qGreen(a[x])-qGreen(b[x]);
			const double blue = qBlue(a[x])-qBlue(b[x]);
			squared += r*r + g*g + blue*blue;
			++loss.pixels;
		}
	}
	// Subpixel/collapsed charts have no measurable raster samples. Retain the
	// footprint fallback instead of claiming lossless reconstruction.
	if(loss.pixels == 0) { loss.error = footprint; return loss; }
	loss.rms = std::sqrt(squared/(3.0*loss.pixels));
	loss.error = footprint*std::min(1.0, loss.rms/calibration);
	return loss;
}
}
#endif
