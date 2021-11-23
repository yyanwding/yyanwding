<template>
	<view>
		<view>
			<!-- <button type="primary" @click="showSchoolPicker">只选择学校</button>
		     -->
			<button style="margin-top:1rem;" type="primary" @click="showSchoolPicker2">省/市/学校</button>

			<view style="margin-top: 1rem;text-align: center;">{{schoolData}}</view>
			<!-- 学校选择组件-->
			<schoolPicker themeColor="#000" ref="schoolPicker" @onConfirm="onConfirm">
			</schoolPicker>

			<schoolPicker :onlySchool='false' themeColor="#000" ref="schoolPicker2" @onConfirm="onConfirm2">
			</schoolPicker>



		</view>
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
	import schoolPicker from '../../components/sugar-schoolPicker/schoolPicker/schoolPicker.vue';
	export default {
		components: {
			optionList,
			schoolPicker
		},
		data() {
			return {
				ip: "127.0.0.1",
				id: '',
				schoolData: '',
				list: [],
				itemHeight: 120, //默认高度120rpx
				options: [ //左滑的操作列表
					// {
					//     color: '#ffffff',
					//     bgColor: '#409EFF',
					//     text: '编辑',
					//     width: 120,
					// },
					{
						color: '#ffffff', //字体颜色，非必须，默认 #ffffff
						bgColor: '#FF4058', //背景颜色，非必须，默认 #409EFF
						text: '删除', //展示文字
						width: 120, //按钮宽度 默认120rpx 适合两个字的宽度 这个宽度按需调整
					}
				],
				threshold: 50,
			}
		},
		methods: {
			listDelete(item, index) {
				console.log('删除');
				console.log(item.id);
				console.log(index);
				// this.list.splice(index, 1);
				// this.list[index]
				var that = this;
				const requestTask = uni.request({
					url: 'http://' + that.ip + ':8181/sc/deleteById',
					data: {
						schoolId: item.id,
						userId: that.id,
					},
					success: function(res) {
						console.log(res.data);
						uni.showToast({
							title: '删除成功',
							duration: 2000,
							icon: 'success'
						});
					}
				});
				uni.reLaunch({
					url: "follow"
				});
			},
			listEdit(item) {
				console.log('编辑');
				console.log(item);
			},
			rowClick(item) {
				console.log('点击某一行');
				console.log(item)
				window.open("http://www.baidu.com")
			},
			optionClick(item, oitem) {
				// console.log('点击某个操作按钮');
				// console.log(item,oitem)
				// if (oitem.text == '删除'){ //这里直接根据text判断点击了哪个按钮，也可自自己增加唯一标识key，当然也可以自己在组件按需定义对应事件
				//     this.listDelete(item);
				// }else if(oitem.text == '编辑'){
				//     this.listEdit(item);
				// }
				this.listDelete(item);
			},
			onShow: function(option) { //option为object类型，会序列化上个页面传递的参数
				var that = this;
				uni.getStorage({
					key: 'user',
					success: function(res) {
						console.log(res.data);
						that.id = res.data.id;
					}
				});
			},
			/**
			 * 打开学校选择器
			 */
			showSchoolPicker: function() {
				console.log(123);
				this.$refs.schoolPicker.show();
			},
			/**
			 * 打开 省/市/学校 选择器
			 */
			showSchoolPicker2: function() {
				this.$refs.schoolPicker2.show();
			},
			/**
			 * 确认学校选择
			 */
			onConfirm(e) {
				const school = e.label.split("-")[2];
				console.log(`源数据:${JSON.stringify(e)}`);
				if (school === '暂未收录') {
					return;
				} else {
					this.schoolData = school;
					console.log(`学校:${school}`);
				}
			},
			/**
			 * 确认 省/市/学校 选择
			 */
			onConfirm2(e) {
				this.schoolData = e.label.split("-").reverse().find(v => v != '所有');
				var that = this;
				const requestTask = uni.request({
					url: 'http://' + that.ip + ':8181/school/queryByText/' + that.schoolData,
					success: function(res) {
						console.log(res.data);
						for (var i = 0; i < res.data.length; i++) {
							res.data[i].index = i;
							res.data[i].img = require('@/static/img/schools/' + res.data[i].id + '.jpg');
						}
						that.list = res.data;
					}
				});
			}
		},
	}
</script>
