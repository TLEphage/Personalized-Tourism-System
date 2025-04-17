<!-- src/components/NavBar.vue -->
 <template>
    <div class="navbar">
        <div class="github-link-container">
            <GitHubLink />
        </div>
        <div class="logo">
            <img v-if="logo" :src="logo" alt="Logo" />
            <span v-else>喵旅游喵</span>
        </div>
        <div class="nav-links">
            <div 
                v-for="(item, index) in navItems"
                :key="index"
                class="nav-item"
                :class="{active :activeIndex === index}"
                @click="handleNavClick(index, item.route)"
            >
                {{ item.name }}
            </div>
        </div>
        <div class="user-actions">
            <!-- 登录/注册按钮  -->
            <div v-if="!isLoggedIn" class="login-btn" @click="handleLoginRegister">登录/注册</div>
            <!-- 用户头像和用户名 -->
            <div v-else class="user-profile" @click="goToUserProfile">
                <img src="" alt="User Avatar" class="avatar" />
                <div class="username">{{ username }}</div>
            </div>
        </div>
    </div>
</template>
<script>
import GitHubLink from './GitHubLink.vue';
import { mapState } from 'vuex'; 
export default{
    name:'NavBar',
    components:{
        GitHubLink,
    },
    props:{
        logo:{
            type:String,
            default:'',
        },
        navItems:{
            type:Array,
            default:()=>[
                {name:'旅游推荐', route:'recommend'},
                {name:'旅游规划', route:'plan'},
                {name:'旅游日记', route:'diary'},
            ]
        },
        isLoggedIn:{
            type:Boolean,
            default:false,
        },
        userAvatar:{
            type:String,
            default:''
        },
        username:{
          type:String,
          default:''
        }
    },
    data(){
        return {
            activeIndex:0,
        }
    },
    computed: {
        ...mapState(['user']),
        // isLoggedIn() {
        //   return this.user.id; // 根据你的用户数据结构判断是否登录
        // },
        // username() {
        //   return this.user.username || '';
        // },
        // userAvatar() {
        //   return this.user.avatarPath || '';
        // }
    },
    methods:{
        handleNavClick(index, route){
            this.activeIndex = index;
            this.$emit('nav-click', route);
            this.$router.push(route);
        },
        handleLoginRegister(){
            this.$router.push({name:'LoginRegister'});
        },
        goToUserProfile(){
            console.log('goToUserProfile');
            this.$router.push({name:'UserProfile'});
            console.log('gotoed');
        }
    }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 50px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.github-link-container {
  position:absolute;
  top:10px;
  left:10px;
  z-index:1001;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.logo img {
  height: 40px;
  margin-right: 10px;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-item {
  cursor: pointer;
  padding: 5px 0;
  position: relative;
  font-size: 16px;
  color: #333;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #1890ff;
}

.nav-item.active {
  color: #1890ff;
  font-weight: 500;
}

.nav-item.active:after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: #1890ff;
}

.user-actions {
  display: flex;
  gap: 15px;
}

.login-btn, .register-btn {
  cursor: pointer;
  padding: 6px 15px;
  border-radius: 4px;
  font-size: 14px;
  transition: all 0.3s;
}

.login-btn {
  color: #1890ff;
  border: 1px solid #1890ff;
}

.login-btn:hover {
  color: #fff;
  background-color: #1890ff;
}

.register-btn {
  color: #fff;
  background-color: #1890ff;
  border: 1px solid #1890ff;
}

.register-btn:hover {
  background-color: #40a9ff;
  border-color: #40a9ff;
}

.user-profile {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-size: 14px;
  color: #333;
}
</style>