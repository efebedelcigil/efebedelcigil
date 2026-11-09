const fs = require('node:fs');
const path = require('node:path');
const { Resvg } = require('@resvg/resvg-js');

const assets=path.join(__dirname,'..','assets');
for(const size of ['', 'mobile-']) {
  for(const theme of ['dark','light']) {
    const name=`hero-${size}${theme}`;
    const source=fs.readFileSync(path.join(assets,name+'-still.svg'));
    const rendered=new Resvg(source).render();
    fs.writeFileSync(path.join(assets,name+'.png'),rendered.asPng());
  }
}
