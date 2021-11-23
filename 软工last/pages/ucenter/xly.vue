<template>
<view>
	<view>
	<option-list :itemHeight="itemHeight" :list="list" :threshold="threshold" @click="rowClick"
		@optionClick="optionClick" :options="options">
		<template slot-scope="{ item }">
			<view class="item">
				<image :src="item.img" mode="aspectFill" class="item-img"></image>
				<text style="margin-left: 20px;">{{item.text}}</text>
			</view>
		</template>
	</option-list>
	</view>
	<view class="u-page">
		
		 <button style="margin-top:1rem;" type="primary" @click="showCalendar(1)">日历</button>
		
		<u-calendar
			:show="show2"
			mode="multiple"
			@confirm="confirm"
			@close="close"
		></u-calendar>
	
		
	</view>
</view>
</template>

<style lang="scss" scoped>
	//scoped 在当前页生效 不影响子组件
	.item {
		// width: 100%;
		padding: 0 20px;
		height: 100%;
		display: flex;
		align-items: center;

		.item-img {
			width: 40px;
			height: 40px;
		}
	}
</style>

<script>
	import optionList from '../../components/gzz-option-list/option-list.vue';
	export default {
		components: {
			optionList
		},
		data() {
			const d = new Date()
			const year = d.getFullYear()
			let month = d.getMonth() + 1
			month = month < 10 ? `0${month}` : month
			const date = d.getDate()
			return {
				index: 0,
							
				show2: false,
				
				
				customThemeDefaultDate: [`${year}-${month}-${date}`, `${year}-${month}-${date + 5}`], 
				customTextDefaultDate: [`${year}-${month}-${date}`],
				maxDate: `${year}-${month}-${date + 10}`,
				defaultDateMultiple: [`${year}-${month}-${date}`, `${year}-${month}-${date + 1}`, `${year}-${month}-${date + 2}`],
				ip: "127.0.0.1",
				id: "",
				list: [],
				itemHeight: 120, //默认高度120rpx
				options: [ //左滑的操作列表
					{
						color: '#ffffff',
						bgColor: '#409EFF',
						text: '关注',
						width: 120,
					},
					// {
					//     color: '#ffffff', //字体颜色，非必须，默认 #ffffff
					//     bgColor: '#FF4058', //背景颜色，非必须，默认 #409EFF
					//     text: '删除', //展示文字
					//     width: 120, //按钮宽度 默认120rpx 适合两个字的宽度 这个宽度按需调整
					// }
				],
				threshold: 50,
			}
		},
		methods: {
			showCalendar(index) {
				this.index = index + 1
				this[`show${index + 1}`] = true
			},
			navigateBack() {
				uni.navigateBack();
			},
			confirm(e) {
				console.log(e);
				this[`show${this.index}`] = false
			},
			close() {
				this[`show${this.index}`] = false
			},
			listDelete(item, index) {
				console.log('删除');
				console.log(item);
				this.list.splice(index, 1);
			},
			listEdit(item) {
				var that = this;
				const requestTask = uni.request({
					url: 'http://' + that.ip + ':8181/sc/add',
					data: {
						userId: that.id,
						schoolId: item.id
					},
					success: function(res) {
						console.log(res.data);
						if (res.data == '已关注') {
							uni.showToast({
								title: '已关注',
								duration: 2000,
								icon: 'error'
							});
						}
						else {
							uni.showToast({
								title: '关注成功',
								duration: 2000,
								icon: 'success'
							});
						}
					}
				});
			},
			rowClick(item) {
				console.log('点击某一行');
				console.log(item)
				plus.runtime.openURL(item.link, function(res) {  
				}); 
				// window.open(item.link);
			},
			optionClick(item, oitem) {
				// console.log('点击某个操作按钮');
				// console.log(item,oitem)
				// if (oitem.text == '删除'){ //这里直接根据text判断点击了哪个按钮，也可自自己增加唯一标识key，当然也可以自己在组件按需定义对应事件
				//     this.listDelete(item);
				// }else if(oitem.text == '编辑'){
				//     this.listEdit(item);
				// }
				this.listEdit(item);
			},
			onShow: function(option) { //option为object类型，会序列化上个页面传递的参数
				var that = this;
				uni.getStorage({
					key: 'user',
					success: function(res) {
						that.id = res.data.id;
					}
				});
				var that = this;
				const requestTask = uni.request({
					url: 'http://' + that.ip + ':8181/school',
					success: function(res) {
						console.log(res.data);
						for (var i = 0; i < res.data.length; i++) {
							res.data[i].img = require('@/static/img/schools/' + res.data[i].id + '.jpg');
						}
						that.list = res.data;
					}
				});
			}
		},
	}
</script>
