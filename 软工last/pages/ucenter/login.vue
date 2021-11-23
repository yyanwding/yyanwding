<template>
	<view class="s-page-wrapper is-100vh">
		<view class="is-33vh has-mgt-10">
			<view class="is-flex is-column is-justify-center  is-align-center is-height-100">
				<image src="../../static/img/common/lg.png" mode="aspectFit" class="logoimg"></image>
			</view>
		</view>
		<view class="content">
			<view class="has-mglr-10 ">
				<view class=" has-mgtb-10 ">
					<input type="text" maxlength="11" v-model="login.username" placeholder="请输入用户名" class="is-input1 "
						@input="BindInput" data-val="phone" />
				</view>
				<view class=" has-radius has-mgtb-10">
					<input v-model="login.password" :password="true" placeholder="请输入登录密码" class="is-input1"
						@input="BindInput" data-val="password" />
				</view>

				<view class=" loginbtn has-radius has-mgtb-20">
					<button :loading="login.loading" @tap="defaultHandlerLogin"> {{ login.loading ? "登录中...":"登 录"}}
					</button>
				</view>
				<view class=" loginbtn has-radius has-mgtb-20" @click="regist()">
					<button>{{"注 册"}}</button>
				</view>

			</view>
		</view>
		<view class="is-20vh has-mgt-80 content">
			<navigator url="#" class=" has-radius is-center is-grey has-mgr-20" hover-class="">
				<text>忘记密码？</text><text class="is-blue">点击找回</text>
			</navigator>
		</view>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				ip: "127.0.0.1",
				login: {
					loading: false,
					username: "",
					password: ""
				},

			};
		},
		methods: {
			defaultHandlerLogin: function() {
				this.login.loading = true;
				setTimeout((e => {
					this.login.loading = false;
				}), 1500);
				this.timer = setTimeout(() => { //设置延迟执行
					var that = this;
					const requestTask = uni.request({
						url: 'http://' + that.ip + ':8181/user/login',
						data: {
							username: that.login.username,
							password: that.login.password
						},
						success: function(res) {
							if (res.data != 0) {
								uni.showToast({
									title: '登录成功',
									duration: 2000,
									icon: 'success'
								});
								uni.setStorage({
									key: 'user',
									data: {
										id: res.data,
										username: that.login.username,
										password: that.login.password
									},
									success: function() {}
								});
								this.timer = setTimeout(() => {
									uni.reLaunch({
										url: "all"
									});
								}, 500);
							} else {
								uni.showToast({
									title: '用户名或密码错误',
									duration: 2000,
									icon: 'error'
								});
							}
						}
					});
				}, 1000);
				// uni.reLaunch({
				// 	url: "follow?id"
				// });
			},
			BindInput: function(e) {
				var dataval = e.currentTarget.dataset.val;
				this.login[dataval] = e.detail.value;
			},
			regist: function() {
				uni.navigateTo({
					url: 'register'
				});
			},
			onShow: function(option) { //option为object类型，会序列化上个页面传递的参数
				uni.getStorage({
					key: 'user',
					success: function(res) {
						console.log(res.data);
						that.login.username = res.data.username;
						that.login.password = res.data.password;
					}
				});
			},
		}
	}
</script>

<style>
	page {
		min-height: 100%;
		background-color: #FFFFFF;
	}

	.content {
		width: 85%;
		margin: 0 auto;
	}

	.loginbtn button {
		margin-top: 20rpx;
		height: 88rpx;
		width: 100%;
		line-height: 88rpx;
		color: #ffffff;
		font-size: 32rpx;
		border-radius: 44rpx;
		outline: 0;
		display: block;
		margin: 0;
		font-family: inherit;
		background: #f35;
		opacity: 0.8;
	}

	button:after {
		border: 2rpx solid #f2f2f2;
	}

	.logoimg {
		width: 200rpx;
		height: 200rpx;
		border-radius: 50%;
	}

	.is-input1 {
		height: 88rpx;
		width: 100%;
		line-height: 88rpx;
		padding: 12rpx;
		color: #353535;
		font-size: 32rpx;
		box-sizing: border-box;
		appearance: none;
		border: 2rpx solid #e5e5e5;
		box-shadow: none;
		border-radius: 44rpx;
		outline: 0;
		display: block;
		padding-left: 30rpx;
		margin: 0;
		font-family: inherit;
		background: #fff;
		resize: none;
	}
</style>
