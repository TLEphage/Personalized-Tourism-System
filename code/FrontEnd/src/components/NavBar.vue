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
            <div class="login-btn" @click="handleLoginRegister">登录/注册meme</div>
        </div>
    </div>
</template>
<script>
import GitHubLink from './GitHubLink.vue';
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
        }
    },
    data(){
        return {
            activeIndex:0,
        }
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
</style>