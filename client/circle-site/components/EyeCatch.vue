<template>
	<div class="eyecatch">
		<section class="eyecatch-image">
			<ul class="eyecatch-image-list">
				<li><img src="@/assets/img/eyecatch.jpg" alt="eyecatch-image"></li>
			</ul>
			<div class="eyecatch-image-overlay"></div>
			<div class="eyecatch-image-content">
				<div class="eyecatch-image-title">
					<h1>
						<ruby><rb>INIAD</rb><rp>(</rp><rt>すべて</rt><rp>)</rp></ruby><span class="japanese">を創ろう。0から、此処から。</span>
					</h1>
				</div>
				<div class="eyecatch-image-logo">
					<p><img src="@/assets/img/logo-square.svg" alt="logo"></p>
				</div>
			</div>
		</section>
		<section class="about">
			<p class="key-image"><img src="@/assets/img/about.svg" alt="about"></p>
			<div class="about-text">
				<p>
					Webメディア研究会は学内の報道機関を目指したサークルです。<br>
					赤羽台キャンパスに関するニュースやお役立ち情報をweb上で発信していきます。<br>
					私たちのサークルは”みんなで作る”ことが魅力のサークルです。<br>
					記事作成・デザイン・システム開発・動画編集等、メンバーそれぞれの得意分野を活かしながら、連携することで様々な活動を行っています。
				</p>
			</div>
		</section>
	</div>
</template>

<script>
export default {
	name: "EyeCatch",
};
</script>

<style lang="scss" scoped>
.eyecatch-image{
	position: relative;
	.eyecatch-image-content{
		position: absolute;
		top: 0;
		left: 0;
		z-index: 3;
		width: 100%;
		height: 100%;
		color: #F0F2FF;
		.eyecatch-image-title{
			display: flex;
			position: absolute;
			width: 100%;
			height: 20%;
			justify-content: center;
			align-items: flex-end;
			font-size: 1.8vw;
			letter-spacing: 0.1em;
			h1{
				display: flex;
				align-items: baseline;
				ruby{
					rb{
						font-size: 1.15em;
						letter-spacing: 0.15em;
					}
					/*
					rt{
						margin-bottom: 0.5em;
						transform: translateY(-0.5em);
					}*/
				}
			}
		}
	}
	ul.eyecatch-image-list{
		padding: 0;
		list-style: none;
		li{
			&::marker{
				display: none;
			}
			margin: 0;
			padding: 0;
			img{
				display: block;
				width: 100%;
			}
		}
	}
	.eyecatch-image-overlay{
		position: absolute;
		top: 0;
		background-color: rgba(#383838, 0.3);
		width: 100%;
		height: 100%;
		z-index: 2;
	}
	.eyecatch-image-logo{
		position: absolute;
		top: 0;
		display: flex;
		width: 100%;
		height: 100%;
		justify-content: center;
		align-items: center;
		z-index: 3;
		p{
			width: 13%;
			height: fit-content;
			img{
				box-shadow: 0 0 1vw 1.5vw rgba(#FFFFFF, 0.5);
			}
		}
	}
}
.about{
	display: flex;
	position: relative;
	margin-top: -4%;
	margin-left: 20%;
	margin-bottom: 3%;
	background-color: #FFFFFF;
	z-index: 5;
	.key-image{
		img{
			margin-left: -15%;
			width: 18vw;
		}
	}
	.about-text{
		margin-top: 6%;
		line-height: 1.8;
		letter-spacing: 1px;
		max-width: 40em;
		font-size: 1.3vw;
	}
}
</style>
