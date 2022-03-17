import React from 'react';
import ReactDOM from 'react-dom';
import { App } from './app';
import { mergeStyles, loadTheme, createTheme, registerIcons } from '@fluentui/react';
import reportWebVitals from './reportWebVitals';
import { SendIcon, SkypeCheckIcon, RedEyeIcon, CheckMarkIcon, HideIcon, CalendarIcon, ChevronUpSmallIcon, ChevronDownSmallIcon, FavoriteStarIcon, FavoriteStarFillIcon, UpIcon, DownIcon, ChevronDownIcon, AreaChartIcon, DonutChartIcon, ScatterChartIcon, BarChartHorizontalIcon, BarChartVerticalIcon, LineChartIcon, ChatBotIcon, MuteChatIcon, CancelIcon, ChevronRightIcon, MoreIcon } from '@fluentui/react-icons-mdl2';
import './index.css';
import { newClient } from './client';


// https://fabricweb.z5.web.core.windows.net/pr-deploy-site/refs/heads/master/theming-designer/
const
  purple = createTheme({
    defaultFontStyle: { fontFamily: '"Source Sans 3"' },
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
    ChevronRight: <ChevronRightIcon />, // used by contextual menu submenu
    FavoriteStar: <FavoriteStarIcon />, // used by rating
    FavoriteStarFill: <FavoriteStarFillIcon />, // used by rating
    Up: <UpIcon />, // used by calendar
    Down: <DownIcon />, // used by calendar
    CheckMark: <CheckMarkIcon />, // used by checkbox
    ChevronDown: <ChevronDownIcon />, // used by dropdown
    Cancel: <CancelIcon />, // used by tag picker
    More: <MoreIcon />, // used by command bar
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

const root = document.getElementById('nitro')
const client = newClient(root?.getAttribute('data-endpoint') ?? '/nitro')
ReactDOM.render(<App client={client} />, root);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
