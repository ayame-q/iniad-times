<template>
	<section class="news-list-wrap">
		<h2>
			<span class="title">News</span>
			<span class="subtitle">最新の活動</span>
		</h2>
		<div class="news-list">
			<ul>
				<li v-for="news of newsList">
					<time>{{ news.date.format("YYYY.MM.DD") }}</time>
					<span class="text">{{ news.title }}</span>
				</li>
			</ul>
			<!--<p class="more-link"><nuxt-link to="news">もっと見る</nuxt-link></p>-->
		</div>
		<div class="clip-polygon"></div>
	</section>
</template>

<script>

export default {
	name: "NewsListSimple",
	data() {
		return {
			newsList: [],
		}
	},
	mounted() {
		const jsonReviver = (key, val) => {
			if (typeof(val) == "string" &&
				val.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{6})?\+\d{2}:\d{2}$/)){
				return this.$dayjs(val);
			}
			if (typeof(val) == "string" &&
				val.match(/^\d{4}-\d{2}-\d{2}$/)){
				return this.$dayjs(val);
			}
			return val;
		}
		fetch("/api/news/")
			.then((response) => response.text())
			.then((responseData) => {
				const result = JSON.parse(responseData, jsonReviver)
				this.newsList = result.slice(0, 5)
			})
	}
};
</script>

<style lang="scss" scoped>
.news-list-wrap{
	display: flex;
	width: 100vw;
	height: calc(100vw / 1920 * 1193);
	overflow: hidden;
	background-image: url("~/assets/img/background-news.jpg");
	background-size: cover;
	position: relative;
	h2{
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		font-weight: 400;
		font-size: 5vw;
		padding: 8vw;
		width: 52vw;
		height: 52vw;
		clip-path: polygon(0 0, 0 100%, 100% 0);
		background-color: #FFFFFF;
		z-index: 3;
		.title{
			letter-spacing: 5px;
		}
		.subtitle{
			margin-left: 10vw;
			font-size: 0.5em;
			&::before{
				content: "-";
				margin-right: 0.2em;
			}
			&::after{
				content: "-";
				margin-left: 0.2em;
			}
		}
	}

	.news-list{
		z-index: 4;
		position: relative;
		margin-left: -18vw;
		margin-top: 18vw;
		color: $circle-color;
		ul{
			list-style: none;
			li{
				font-size: 1.2vw;
				background-color: #FFFFFF;
				border-radius: 10em;
				padding: 1em 3.5em;
				margin: 1.2em 0;
				display: flex;
				align-items: baseline;
				width: 28em;
				box-shadow: 1em 0.8em rgba($key-color, 0.42);
				time{
					display: block;
					width: 6em;
				}

				&:nth-child(2){
					margin-left: 5em;
				}
				&:nth-child(3){
					margin-left: 10em;
				}
				&:nth-child(4){
					margin-left: 15em;
				}
				&:nth-child(5){
					margin-left: 20em;
				}
			}
		}
		.more-link {
			text-align: right;
			margin-top: 3em;
			a{
				font-size: 1.5vw;
				color: #FFFFFF;
				padding: 0.4em 0.6em;
				border: #FFFFFF solid 2px;
			}
		}
	}

	.clip-polygon{
		z-index: 1;
		position: absolute;
		bottom: 0;
		width: 52vw;
		height: 52vw;
		clip-path: polygon(0 0, 0 100%, 100% 100%);
		background-color: rgba(#FFFFFF, 0.35);
	}
}
</style>
