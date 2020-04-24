import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home';

// Codewords View
import CodewordsHome from '@/views/codewords/CodewordsHome';
import Help from '@/views/codewords/Help';
import Create from '@/views/codewords/Create';
import Player from '@/views/codewords/Player';
import Spymaster from '@/views/codewords/Spymaster';

// Spyfall View
import SpyfallHome from '@/views/spyfall/SpyfallHome';
import SpyfallLobby from '@/views/spyfall/SpyfallLobby';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
      // Codewords
    {
      path: '/codewords',
      name: 'CodewordsHome',
      component: CodewordsHome,
    },
    {
      path: '/create',
      name: 'Create',
      component: Create,
    },
    {
      path: '/help',
      name: 'Help',
      component: Help,
    },
    {
      path: '/:room/player',
      name: 'Player',
      component: Player,
    },
    {
      path: '/:room/spymaster',
      name: 'Spymaster',
      component: Spymaster,
    },
      // Spyfall
    {
      path: '/spyfall',
      name: 'SpyfallHome',
      component: SpyfallHome,
    },
    {
      path: '/spyfall/lobby',
      name: 'SpyfallLobby',
      component: SpyfallLobby,
    },
  ],
});
