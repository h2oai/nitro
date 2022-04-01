//
// This script scans index.d.ts in the react-icons-mdl2 package and generates icons.tsx.
// 
// The default icon package that ships with Fluent contains Microsoft-proprietary 
// brand icons that are not licensed for use on non-Office sites.
// 
// The react-icons-mdl2 package does not contain branded icons as of this writing.
//
// Source: https://developer.microsoft.com/en-us/fluentui#/styles/web/icons
// "An SVG-based version of Fluent UI's icon set is available from @fluentui/react-icons-mdl2 and 
// is released under the MIT license. This is the same MDL2 icon set used in the font icons, 
// excluding any branded icons."

const
  fs = require('fs'),
  codePath = 'web/src/icons.tsx',
  libPath = 'web/node_modules/@fluentui/react-icons-mdl2/lib/index.d.ts',
  libCode = fs.readFileSync(libPath, { encoding: 'utf8' }),
  icons = [...libCode.matchAll(/default as ([A-Z]\w+)Icon/g)].map(m => m[1]),
  importing = icons.map(x => `  ${x}Icon,`),
  listing = icons.map(x => `  ${x}: <${x}Icon />,`),
  code = [
    'import {',
    importing.join('\n'),
    "} from '@fluentui/react-icons-mdl2'",
    '',
    'export const icons = {',
    listing.join('\n'),
    '}',
    ''
  ].join('\n')

fs.writeFileSync(codePath, code, { encoding: 'utf8' })

console.log(`Success! ${icons.length} icons written to ${codePath}`)
