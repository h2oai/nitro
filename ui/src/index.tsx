import React from 'react';
import ReactDOM from 'react-dom';
import { App } from './app';
import { mergeStyles, loadTheme, createTheme, registerIcons } from '@fluentui/react';
import reportWebVitals from './reportWebVitals';
import { SendIcon, SkypeCheckIcon, RedEyeIcon, CheckMarkIcon, HideIcon, CalendarIcon, ChevronUpSmallIcon, ChevronDownSmallIcon, FavoriteStarIcon, FavoriteStarFillIcon, UpIcon, DownIcon, ChevronDownIcon, AreaChartIcon, DonutChartIcon, ScatterChartIcon, BarChartHorizontalIcon, BarChartVerticalIcon, LineChartIcon, ChatBotIcon, MuteChatIcon, CancelIcon } from '@fluentui/react-icons-mdl2';
import './index.css';
import { newSidekick } from './sidekick';


// https://fabricweb.z5.web.core.windows.net/pr-deploy-site/refs/heads/master/theming-designer/
const
  purple = createTheme({
    defaultFontStyle: { fontFamily: 'Roboto' },
    palette: {
      themePrimary: '#4a00e0',
      themeLighterAlt: '#f7f4fe',
      themeLighter: '#dfd2fa',
      themeLight: '#c5acf6',
      themeTertiary: '#8e5fed',
      themeSecondary: '#5e1be4',
      themeDarkAlt: '#4300ca',
      themeDark: '#3900ab',
      themeDarker: '#2a007e',
      neutralLighterAlt: '#faf9f8',
      neutralLighter: '#f3f2f1',
      neutralLight: '#edebe9',
      neutralQuaternaryAlt: '#e1dfdd',
      neutralQuaternary: '#d0d0d0',
      neutralTertiaryAlt: '#c8c6c4',
      neutralTertiary: '#a19f9d',
      neutralSecondary: '#605e5c',
      neutralPrimaryAlt: '#3b3a39',
      neutralPrimary: '#323130',
      neutralDark: '#201f1e',
      black: '#000000',
      white: '#ffffff',
    }
  });

loadTheme(purple)

registerIcons({
  icons: {
    Send: <SendIcon />, // used by message-send button
    SkypeCheck: <SkypeCheckIcon />, // not used directly, but Fluent throws warnings if not defined
    RedEye: <RedEyeIcon />, // used by password text field
    Hide: <HideIcon />, // used by password text field
    Calendar: <CalendarIcon />, // used by password text field
    ChevronUpSmall: <ChevronUpSmallIcon />, // used by spin button
    ChevronDownSmall: <ChevronDownSmallIcon />, // used by spin button
    FavoriteStar: <FavoriteStarIcon />, // used by rating
    FavoriteStarFill: <FavoriteStarFillIcon />, // used by rating
    Up: <UpIcon />, // used by calendar
    Down: <DownIcon />, // used by calendar
    CheckMark: <CheckMarkIcon />, // used by checkbox
    ChevronDown: <ChevronDownIcon />, // used by dropdown
    Cancel: <CancelIcon />, // used by tag picker
    // Used by examples
    AreaChart: <AreaChartIcon />,
    BarChartHorizontal: <BarChartHorizontalIcon />,
    BarChartVertical: <BarChartVerticalIcon />,
    LineChart: <LineChartIcon />,
    ScatterChart: <ScatterChartIcon />,
    DonutChart: <DonutChartIcon />,
    ChatBot: <ChatBotIcon />,
    MuteChat: <MuteChatIcon />,
  },
})

const sidekick = newSidekick()
ReactDOM.render(<App sidekick={sidekick} />, document.getElementById('root'));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
