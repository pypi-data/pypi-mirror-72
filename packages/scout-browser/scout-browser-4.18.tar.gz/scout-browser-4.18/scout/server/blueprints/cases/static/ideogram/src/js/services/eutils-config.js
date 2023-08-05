// The E-Utilies In Depth: Parameters, Syntax and More:
// https://www.ncbi.nlm.nih.gov/books/NBK25499/
var eutils = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
var esearch = eutils + 'esearch.fcgi?retmode=json';
var esummary = eutils + 'esummary.fcgi?retmode=json';
var elink = eutils + 'elink.fcgi?retmode=json';

function getAssemblySearchUrl(ideo) {
  var organism, termStem, asmSearchUrl;

  organism = ideo.config.organism;

  if (ideo.assemblyIsAccession()) {
    termStem = ideo.config.assembly + '%22[Assembly%20Accession]';
  } else {
    termStem = (
      organism + '%22[organism]' +
      'AND%20(%22latest%20refseq%22[filter])%20'
    );
  }

  asmSearchUrl =
    ideo.esearch +
    '&db=assembly' +
    '&term=%22' + termStem +
    'AND%20(%22chromosome%20level%22[filter]%20' +
    'OR%20%22complete%20genome%22[filter])';

  return asmSearchUrl;
}

export {esearch, esummary, elink, getAssemblySearchUrl}