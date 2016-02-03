var bodyElem = d3.select('body'),
    jsElem = d3.select('#js'),
    jsPanel = bodyElem.append('div').attr('id', 'jsPanel');
    cssElem = d3.select('#css'),
    cssPanel = bodyElem.append('div').attr('id', 'cssPanel');

function setupPanel(panel, elem, title) {
  panel.append('h2').text(title);
  return panel.append('pre').append('code').text(elem.html().trim());
}

bodyElem.append('link')
  .attr('rel', 'stylesheet')
  .attr('href',  'xcode.min.css');
bodyElem.append('script')
  .attr('src',  'highlight.min.js')
  .on('load', function() {
    
  });
