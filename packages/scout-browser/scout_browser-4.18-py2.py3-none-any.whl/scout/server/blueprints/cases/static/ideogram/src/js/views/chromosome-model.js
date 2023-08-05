function getPixelAndOtherData(bands, chr, hasBands, ideo) {
  var i, band, csLength, width, cs,
    pxStop = 0,
    cs = ideo.coordinateSystem,
    chrHeight = ideo.config.chrHeight;

  for (var i = 0; i < bands.length; i++) {
    band = bands[i];
    csLength = band[cs].stop - band[cs].start;

    // If ideogram is rotated (and thus showing only one chromosome),
    // then set its width independent of the longest chromosome in this
    // genome.
    if (ideo._layout._isRotated) {
      width = chrHeight * csLength / chr.length;
    } else {
      width = chrHeight * chr.length / ideo.maxLength[cs] * csLength / chr.length;
    }
    bands[i].px = {start: pxStop, stop: pxStop + width, width: width};

    pxStop = bands[i].px.stop;

    if (hasBands && band.stain === 'acen' && band.name[0] === 'p') {
      chr.pcenIndex = i;
    }
  }
  return [bands, chr, pxStop];
}

/**
 * TODO:
 * A chromosome-level scale property is likely
 * nonsensical for any chromosomes that have cytogenetic band data.
 * Different bands tend to have ratios between number of base pairs
 * and physical length.
 *
 * However, a chromosome-level scale property is likely
 * necessary for chromosomes that do not have band data.
 *
 * This needs further review.
 */
function getChrScale(chr, hasBands, ideo) {
  var chrHeight = ideo.config.chrHeight,
    chrLength = chr.length,
    maxLength = ideo.maxLength,
    scale = {}

  if (ideo.config.multiorganism === true) {
    scale.bp = 1;
    // chr.scale.bp = band.iscn.stop / band.bp.stop;
    scale.iscn = chrHeight * chrLength / maxLength.bp;
  } else {
    scale.bp = chrHeight / maxLength.bp;
    if (hasBands) {
      scale.iscn = chrHeight / maxLength.iscn;
    }
  }

  return scale;
}

function getChromosomePixels(chr) {
  var bands, chrHeight, pxStop, hasBands,
    ideo = this;

  bands = chr.bands;
  chrHeight = ideo.config.chrHeight;
  pxStop = 0;
  hasBands = (typeof bands !== 'undefined');

  if (hasBands) {
    [bands, chr, pxStop] = getPixelAndOtherData(bands, chr, hasBands, ideo);
  } else {
    pxStop = chrHeight * chr.length / ideo.maxLength[ideo.coordinateSystem];
  }

  chr.width = pxStop;
  chr.scale = getChrScale(chr, hasBands, ideo);
  chr.bands = bands;

  return chr;
}

function getChrModelScaffold(chr, bands, chrName, ideo) {
  var hasBands = (typeof bands !== 'undefined');

  if (hasBands) {
    chr.name = chrName;
    chr.length = bands[bands.length - 1][ideo.coordinateSystem].stop;
    chr.type = 'nuclear';
  } else {
    chr = chrName;
  }

  return chr;
}

/**
 * Encountered when processing an assembly that has chromosomes with
 * centromere data, but this chromosome does not.
 * Example: chromosome F1 in Felis catus.
 */
function deleteExtraneousBands(chr, hasBands) {
  if (hasBands && chr.bands.length === 1) {
    delete chr.bands;
  }
  return chr;
}

function getCentromerePosition(hasBands, bands) {
  if (
    hasBands && bands[0].name[0] === 'p' && bands[1].name[0] === 'q' &&
    bands[0].bp.stop - bands[0].bp.start < 2E6
  ) {
    // As with almost all mouse chromosome, chimpanzee chr22
    return 'telocentric';
  } else {
    return '';
  }
}

/**
 * Generates a model object for each chromosome containing information on
 * its name, DOM ID, length in base pairs or ISCN coordinates, cytogenetic
 * bands, centromere position, etc.
 */
function getChromosomeModel(bands, chrName, taxid, chrIndex) {
  var hasBands,
    chr = {},
    ideo = this;

  hasBands = (typeof bands !== 'undefined');

  chr = getChrModelScaffold(chr, bands, chrName, ideo)

  chr.chrIndex = chrIndex;
  chr.id = 'chr' + chr.name + '-' + taxid;

  if (ideo.config.fullChromosomeLabels === true) {
    var orgName = this.organisms[taxid].scientificNameAbbr;
    chr.name = orgName + ' chr' + chr.name;
  }

  chr.bands = bands;
  chr = ideo.getChromosomePixels(chr);
  chr.centromerePosition = getCentromerePosition(hasBands, bands);

  chr = deleteExtraneousBands(chr, hasBands);

  return chr;
}

export {getChromosomeModel, getChromosomePixels};