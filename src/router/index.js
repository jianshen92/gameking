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
import SpyfallGame from '@/views/spyfall/SpyfallGame';

// Doudizhu View
import DouDiZhuHome from '@/views/doudizhu/DouDiZhuHome';
import DouDiZhuLobby from '@/views/doudizhu/DouDiZhuLobby';
import DouDiZhuGame from '@/views/doudizhu/DouDiZhuGame';

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
    {
      path: '/spyfall/game',
      name: 'SpyfallGame',
      component: SpyfallGame,
    },
    // Doudizhu
    {
      path: '/doudizhu',
      name: 'DouDiZhuHome',
      component: DouDiZhuHome
    },
    {
      path: '/doudizhu/lobby',
      name: 'DouDiZhuLobby',
      component: DouDiZhuLobby
    },
    {
      path: '/doudizhu/game',
      name: 'DouDiZhuGame',
      component: DouDiZhuGame
    }
  ],
});
