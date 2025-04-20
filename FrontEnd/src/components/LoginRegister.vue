<!-- src/components/LoginRegister.vue -->
<template>
    <div class="login-register">
        <div class="contain">
            <div class="big-box" :class="{active:isLogin}">
                <div class="big-contain" key="bigContainLogin" v-if="isLogin">
                    <div class="btitle">账户登录</div>
                    <div class="bform">
                        <!--placeholder为占位符 v-model为输入框和form.useremail双向绑定-->
                        <input type="text" placeholder="用户名" v-model="form.username">
                        <span class="errTips" v-if="usernameError">* 用户名不存在</span>
                        <input type="password" placeholder="密码" v-model="form.userpwd">
                        <span class="errTips" v-if="passwordError">* 密码填写错误</span>
                    </div>
                    <button class="bbutton" @click="login">登录</button>
                </div>
                <div class="big-contain" key="igContainRegister" v-else>
                    <div class="btitle">创建账户</div>
                    <div class="bform">
                        <input type="text" placeholder="用户名" v-model="form.username">
                        <span class="errTips" v-if="existed">* 用户名已经存在</span>
                        <!-- <input type="email" placeholder="邮箱" v-model="form.useremail"> -->
                        <input type="password" placeholder="密码" v-model="form.userpwd">
                    </div>
                    <button class="bbutton" @click="register">注册</button>
                </div>
            </div>
            <div class="small-box" :class="{active:isLogin}">
                <div class="small-contain" key="smallContainRegister" v-if="isLogin">
                    <div class="stitle">你好，朋友！</div>
                    <p class="scontent">开始注册，和我们一起旅行</p>
                    <button class="sbutton" @click="changeType">注册</button>
                </div>
                <div class="small-contain" key="smallContainLogin" v-else>
                    <div class="stitle">欢迎回来！</div>
                    <p class="scontent">与我们保持联系，请登录你的账户</p>
                    <button class="sbutton" @click="changeType">登录</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {useStore} from 'vuex';
export default {
    name: 'LoginRegister',
	setup() {
		const store = useStore();
		return {
			store
		};
	},
    data () {
        return {
            isLogin:false,
            emailError:false,
            passwordError:false,
            existed:false,
            form: {
                username: '',
                useremail: '',
                userpwd: ''
            }
        }
    },
    methods: {
        changeType () {
            this.isLogin = !this.isLogin;
            this.form.username = '';
            this.form.useremail = '';
            this.form.userpwd = '';
        },
        login() {
			const self = this;
			if (self.form.username !== "" && self.form.userpwd !== "") {
				axios.post('http://localhost:8000/users/login', {
					username: self.form.username,
					password: self.form.userpwd,
				})
				.then(res => {
					console.log(res.data);
					// 检查后端返回的用户数据
					if (res.data.id) { // 如果有id，表示登录成功
						alert("登录成功！");
						//存储用户信息到Vuex store 或本地存储
						self.store.commit('setUser', res.data);
						//通知导航栏更新
						self.$emit('user-login', {
							isLoggedIn:true,
							username:res.data.username,
							userAvatar:res.data.avatarPath,
						});
						if (res.data.hobbies) { // 如果有兴趣信息，跳转到旅游推荐
							self.$router.push({name: 'Recommend'});
						} else {
							self.$router.push({name: 'InterestSelector'});
						}
					} else {
						// 如果没有 token，可能是后端返回了错误信息
						alert("用户名或密码错误！");
					}
				})
				.catch(err => {
					console.log(err);
					// 捕获网络请求错误或后端抛出的异常
					if (err.response && err.response.data) {
						// 如果后端抛出了 HTTPException，通常会在 err.response.data 中返回错误信息
						alert("登录失败：" + err.response.data.detail);
					} else {
						// 其他网络错误
						alert("登录失败：网络错误");
					}
					console.error(err);
				});
			} else {
				alert("填写不能为空！");
			}
		},
        register () {
            const self = this;
            if(self.form.username != ""  && self.form.userpwd != "") {
                axios.post('http://localhost:8000/users/register', {
						username: self.form.username,
						password: self.form.userpwd
                })
                .then(
                    res => {
                        if(res.data.message === "注册成功"){
							alert("注册成功！");
							this.isLogin = true;
						} else {
							this.existed = true;
							alert("用户名已存在");
						}
                    }
                )
                .catch(
                    err => {
					// 捕获网络请求错误或后端抛出的异常
					if (err.response && err.response.data) {
						// 如果后端抛出了 HTTPException，通常会在 err.response.data 中返回错误信息
						alert("注册失败：" + err.response.data.detail);
					} else {
						// 其他网络错误
						alert("登录失败：网络错误");
					}
					console.error(err);
				}
                )
            } else {
                alert("填写不能为空！");
            }
        }
    }
}
</script>


<style scoped="scoped">
	.login-register{
		width: 100vw;
		height: 100vh;
		box-sizing: border-box;
		position: fixed;
		top:0;
		left:0;
	}
	.contain{
		width: 60%;
		height: 60%;
		position: relative;
		top: 50%;
		left: 50%;
		transform: translate(-50%,-50%);
		background-color: #fff;
		border-radius: 20px;
		box-shadow: 0 0 3px #f0f0f0,
					0 0 6px #f0f0f0;
	}
	.big-box{
		width: 70%;
		height: 100%;
		position: absolute;
		top: 0;
		left: 30%;
		transform: translateX(0%);
		transition: all 1s;
	}
	.big-contain{
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.btitle{
		font-size: 1.5em;
		font-weight: bold;
		color: rgb(57,167,176);
	}
	.bform{
		width: 100%;
		height: 40%;
		padding: 2em 0;
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		align-items: center;
	}
	.bform .errTips{
		display: block;
		width: 50%;
		text-align: left;
		color: red;
		font-size: 0.7em;
		margin-left: 1em;
	}
	.bform input{
		width: 50%;
		height: 30px;
		border: none;
		outline: none;
		border-radius: 10px;
		padding-left: 2em;
		background-color: #f0f0f0;
	}
	.bbutton{
		width: 20%;
		height: 40px;
		border-radius: 24px;
		border: none;
		outline: none;
		background-color: rgb(57,167,176);
		color: #fff;
		font-size: 0.9em;
		cursor: pointer;
	}
	.small-box{
		width: 30%;
		height: 100%;
		background: linear-gradient(135deg,rgb(57,167,176),rgb(56,183,145));
		position: absolute;
		top: 0;
		left: 0;
		transform: translateX(0%);
		transition: all 1s;
		border-top-left-radius: inherit;
		border-bottom-left-radius: inherit;
	}
	.small-contain{
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}
	.stitle{
		font-size: 1.5em;
		font-weight: bold;
		color: #fff;
	}
	.scontent{
		font-size: 0.8em;
		color: #fff;
		text-align: center;
		padding: 2em 4em;
		line-height: 1.7em;
	}
	.sbutton{
		width: 60%;
		height: 40px;
		border-radius: 24px;
		border: 1px solid #fff;
		outline: none;
		background-color: transparent;
		color: #fff;
		font-size: 0.9em;
		cursor: pointer;
	}
	
	.big-box.active{
		left: 0;
		transition: all 0.5s;
	}
	.small-box.active{
		left: 100%;
		border-top-left-radius: 0;
		border-bottom-left-radius: 0;
		border-top-right-radius: inherit;
		border-bottom-right-radius: inherit;
		transform: translateX(-100%);
		transition: all 1s;
	}
</style>