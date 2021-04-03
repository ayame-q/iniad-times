<template>
	<section class="circle-info-wrap">
		<div class="circle-info">
			<h2>
				<span class="title">Info</span>
				<span class="subtitle">サークル概要</span>
			</h2>
			<dl>
				<dt>サークル名</dt>
				<dd>Webメディア研究会</dd>
				<dt>所属キャンパス</dt>
				<dd>東洋大学赤羽台キャンパス</dd>
				<dt>代表</dt>
				<dd>立松 あやめ</dd>
				<dt>顧問</dt>
				<dd>淺野 智之 先生</dd>
				<dt>部員数</dt>
				<dd>22名</dd>
				<dt>メールアドレス</dt>
				<dd>info@iniad-wm.com</dd>
			</dl>
		</div>
		<div class="logo">
			<p><img src="@/assets/img/logo-square.svg" alt="Logo"></p>
		</div>
	</section>
</template>

<script>
export default {
	name: "CircleInfo",
};
</script>

<style lang="scss" scoped>
.circle-info-wrap{
	display: flex;
	margin: 12vw;
	.circle-info{
		flex-basis: 50%;
		h2{
			display: flex;
			align-items: center;
			font-weight: 400;
			font-size: 4.5vw;
			border-bottom: $circle-color solid 2px;
			.title{
				letter-spacing: 5px;
			}
			.subtitle{
				margin-left: 3vw;
				margin-top: 1vw;
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

		dl{
			display: flex;
			flex-wrap: wrap;
			line-height: 2.5;
			font-size: 1.5vw;
			padding: 1em;
			margin-top: 1em;
			dt{
				width: 40%;
			}
			dd{
				width: 60%;
			}
		}
	}
	.logo{
		flex-basis: 45%;
		margin-left: 5%;
		display: flex;
		justify-content: center;
		margin-top: 6vw;
		img{
			width: 20vw;
		}
	}
}
</style>
