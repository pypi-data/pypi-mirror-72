import * as d3selection from 'd3-selection';

import {ModelAdapter} from '../model-adapter';
import {Chromosome} from './chromosome';

var d3 = Object.assign({}, d3selection);

/**
 * Adds a copy of a chromosome (i.e. a homologous chromosome, homolog) to DOM
 *
 * @param chrModel
 * @param chrIndex
 * @param homologIndex
 * @param container
 */
function appendHomolog(chrModel, chrIndex, homologIndex, container) {

  var homologOffset, chromosome, shape, defs, adapter;

  defs = d3.select(this.selector + ' defs');
  // Get chromosome model adapter class
  adapter = ModelAdapter.getInstance(chrModel);

  // How far this copy of the chromosome is from another
  homologOffset = homologIndex * this.config.chrMargin;

  // Append chromosome's container
  chromosome = container
    .append('g')
    .attr('id', chrModel.id)
    .attr('class', 'chromosome ' + adapter.getCssClass())
    .attr('transform', 'translate(0, ' + homologOffset + ')');

  // Render chromosome
  shape = Chromosome.getInstance(adapter, this.config, this)
    .render(chromosome, chrIndex, homologIndex);

  d3.select('#' + chrModel.id + '-chromosome-set-clippath').remove();

  defs.append('clipPath')
    .attr('id', chrModel.id + '-chromosome-set-clippath')
    .selectAll('path')
    .data(shape)
    .enter()
    .append('path')
    .attr('d', function (d) {
      return d.path;
    })
    .attr('class', function (d) {
      return d.class;
    });
}


/**
 * Renders all the bands and outlining boundaries of a chromosome.
 */
function drawChromosome(chrModel) {

  var chrIndex, container, numChrsInSet, transform, homologIndex,
    chrSetSelector;

  chrIndex = chrModel.chrIndex;

  transform = this._layout.getChromosomeSetTranslate(chrIndex);

  chrSetSelector = this.selector + ' #' + chrModel.id + '-chromosome-set';

  d3.selectAll(chrSetSelector + ' g').remove();

  container = d3.select(chrSetSelector);

  if (container.nodes().length === 0) {
    // Append chromosome set container
    container = d3.select(this.selector)
      .append('g')
      .attr('class', 'chromosome-set-container')
      .attr('data-set-number', chrIndex)
      .attr('transform', transform)
      .attr('id', chrModel.id + '-chromosome-set');
  }

  if (
    'sex' in this.config &&
    this.config.ploidy === 2 &&
    this.sexChromosomes.index === chrIndex
  ) {
    this.drawSexChromosomes(container, chrIndex);
    return;
  }

  numChrsInSet = 1;
  if (this.config.ploidy > 1) {
    numChrsInSet = this._ploidy.getChromosomesNumber(chrIndex);
  }

  for (homologIndex = 0; homologIndex < numChrsInSet; homologIndex++) {
    this.appendHomolog(chrModel, chrIndex, homologIndex, container);
  }
}

/**
 * Rotates a chromosome 90 degrees and shows or hides all other chromosomes
 * Useful for focusing or defocusing a particular chromosome
 */
function rotateAndToggleDisplay(chrElement) {

  var chrName, chrModel, chrIndex, chrSetIndex;

  // Do nothing if taxid not defined. But it should be defined.
  // To fix that bug we should have a way to find chromosome set number.
  if (!this.config.taxid) {
    return;
  }

  chrName = chrElement.id.split('-')[0].replace('chr', '');
  chrModel = this.chromosomes[this.config.taxid][chrName];
  chrIndex = chrModel.chrIndex;

  chrSetIndex =
    Number(d3.select(chrElement.parentNode).attr('data-set-number'));

  this._layout.rotate(chrSetIndex, chrIndex, chrElement);
}

function setOverflowScroll() {
  var ideo, config, ideoWidth, ideoInnerWrap, ideoOuterWrap, ideoSvg,
    ploidy, ploidyPad;

  ideo = this;
  config = ideo.config;

  ideoSvg = d3.select(config.container + ' svg#_ideogram');
  ideoInnerWrap = d3.select(config.container + ' #_ideogramInnerWrap');
  ideoOuterWrap = d3.select(config.container + ' #_ideogramOuterWrap');

  ploidy = config.ploidy;
  ploidyPad = (ploidy - 1);

  if (
    config.orientation === 'vertical' &&
    config.perspective !== 'comparative'
  ) {
    ideoWidth = (ideo.numChromosomes + 2) * (config.chrWidth + config.chrMargin + ploidyPad);
  } else {
    return;
    // chrOffset = ideoSvg.select('.chromosome').nodes()[0].getBoundingClientRect();
    // ideoWidth = config.chrHeight + chrOffset.x + 1;
  }

  ideoWidth = Math.round(ideoWidth * ploidy / config.rows);

  // Ensures absolutely-positioned elements, e.g. heatmap overlaps, display
  // properly if ideogram container also has position: absolute
  ideoOuterWrap
    .style('height', ideo._layout.getHeight() + 'px')

  ideoInnerWrap
    .style('max-width', ideoWidth + 'px')
    .style('overflow-x', 'scroll')
    .style('position', 'absolute');
  ideoSvg.style('min-width', (ideoWidth - 5) + 'px');
}

export {
  appendHomolog, drawChromosome, rotateAndToggleDisplay, setOverflowScroll
}