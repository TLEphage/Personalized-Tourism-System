import { createRouter,createWebHashHistory } from 'vue-router'
import Recommend from './views/Recommend.vue'
import Plan from './views/Plan.vue'
import Diary from './views/Diary.vue'
import LoginRegister from './components/LoginRegister.vue'
import InterestSelector from './components/InterestSelector.vue'
import UserProfile from './components/UserProfile.vue'
import Developer from './views/Developer.vue'
import SpotDetail from './components/SpotDetail.vue'
import DiaryDetail from './components/DiaryDetail.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes:[
        {
            path: '/Recommend',
            name:'Recommend',
            component:Recommend
        },
        {
            path: '/Plan',
            name:'Plan',
            component:Plan
        },
        {
            path: '/Diary',
            name:'Diary',
            component:Diary
        },
        {
            path: '/LoginRegister',
            name:'LoginRegister',
            component:LoginRegister
        },
        {
            path:'/InterestSelector',
            name:'InterestSelector',
            component:InterestSelector,
        },
        {
            path:'/UserProfile',
            name:'UserProfile',
            component:UserProfile
        },
        {
            path:'/Developer',
            name:'Developer',
            component:Developer
        },
        {
            path:'/SpotDetail/:name',
            name:'SpotDetail',
            component:SpotDetail
        },
        {
            path:'/DiaryDetail/:id',
            name:'DiaryDetail',
            component:DiaryDetail
        }
    ]
});

export default router;