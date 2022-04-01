import { createTheme, loadTheme, registerIcons } from '@fluentui/react';
import React from 'react';
import ReactDOM from 'react-dom';
import { App } from './app';
import { newClient } from './client';
import { icons } from './icons';
import './index.css';
import reportWebVitals from './reportWebVitals';


// https://fabricweb.z5.web.core.windows.net/pr-deploy-site/refs/heads/master/theming-designer/
const
  purple = createTheme({
    defaultFontStyle: { fontFamily: '"Source Sans 3"' },
  });

loadTheme(purple)
registerIcons({ icons })

const root = document.getElementById('nitro')
const client = newClient(root?.getAttribute('data-endpoint') ?? '/nitro')
ReactDOM.render(<App client={client} />, root);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
