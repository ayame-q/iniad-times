<template>
	<section class="activities">
		<h2>
			<span class="title">Activities</span>
			<span class="subtitle">活動の紹介</span>
		</h2>
		<section class="times">
			<div class="eyecatch-wrap">
				<div class="eyecatch">
					<img src="~/assets/img/times-logo-white.svg" alt="INIAD Times">
				</div>
			</div>
			<div class="content-wrap">
				<h3>
					<span class="title">INIAD Times</span>
				</h3>
				<div class="content">
					<p class="comment">
						Webメディア研究会の最もメインの活動です。<br>
						サークルや授業・イベント・お役立ち情報を学内に向けて発信していきます。
					</p>
					<p class="link"><a href="https://iniad-wm.com"><img src="~/assets/img/times-icon-small-white.svg" alt="icon">INIAD Timesトップページ</a></p>
				</div>
			</div>
		</section>
		<section class="meets">
			<div class="eyecatch-wrap">
				<div class="eyecatch">
					<img src="~/assets/img/meets-logo.svg" alt="INIAD meets web">
				</div>
			</div>
			<div class="content-wrap">
				<h3>
					<span class="title">INIAD meets web</span>
				</h3>
				<div class="content">
					<p class="comment">
						INIADの公認サークルが集ってオンライン上で行う新入生歓迎会イベントです。<br>
						参加者の方々やサークルの方々のご協力もあり、2020年度の新入生の6割以上もの一年生にご参加いただきました。<br>
						大学学部や事務課の協力の下、当サークル主催で開催しています。
					</p>
					<p class="link"><a href="https://meets.iniad.net"><img src="~/assets/img/meets-logo-square-2.svg" alt="icon">INIAD meets webサイト</a></p>
				</div>
			</div>
		</section>
		<div class="clip-polygon"></div>
	</section>
</template>

<script>
export default {
	name: "Activities",
};
</script>

<style lang="scss" scoped>
.activities{
	background-color: rgba($circle-color, 0.1);
	overflow: hidden;
	position: relative;

	h2{
		display: flex;
		align-items: center;
		font-weight: 400;
		font-size: 5vw;
		margin: 10vw;
		margin-top: 20vw;
		.title{
			letter-spacing: 5px;
		}
		.subtitle{
			margin-left: 3vw;
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

	section{
		display: flex;
		margin: 10vw 0;
		.eyecatch-wrap{
			width: 40vw;
			background-color: rgba($circle-color, 0.7);
			.eyecatch{
				display: flex;
				justify-content: center;
				align-items: center;
				margin-top: 8vw;
				width: 40vw;
				height: calc(100% - 8vw);
				min-height: 30vw;
				background-color: $circle-color;
				overflow: hidden;
				img{
					width: 30vw;
				}
			}
		}

		.content-wrap{
			margin: 0 5vw;
			width: 100%;
			h3{
				height: 8vw;
				font-size: 4.2vw;
				font-weight: 400;
				border-bottom: $circle-color 2px solid;
			}
			.content{
				display: flex;
				flex-direction: column;
				justify-content: stretch;
				height: calc(100% - 8vw);
				.comment{
					padding: 0 1em;
					flex-grow: 1;
					display: flex;
					align-items: center;
					line-height: 2;
					letter-spacing: 0.8px;
					font-size: 1.5vw;
				}
				.link{
					margin-left: auto;
					margin-right: 0;
					a{
						font-size: 1.2vw;
						display: flex;
						align-items: center;
						flex-grow: 0;
						color: white;
						background-color: $circle-color;
						border-radius: 8px;
						padding: 5px 10px;
						padding-right: 15px;
						margin-bottom: 10px;
						white-space: nowrap;
						img{
							height: 2em;
						}
					}
				}
			}
		}

		&:nth-child(2n){
			.eyecatch-wrap{
				margin-right: 8vw;
				.eyecatch{
					margin-left: 8vw;
				}
			}
			.content-wrap{
				h3{
					background-image: url("~/assets/img/activities-icon-right.svg");
					background-position: right 90%;
					background-repeat: no-repeat;
					background-size: 3vw;
					span.title{
						margin-left: -10vw;
					}
				}
			}
		}

		&:nth-child(2n+1){
			flex-direction: row-reverse;
			.eyecatch-wrap{
				margin-left: 8vw;
				.eyecatch{
					margin-left: -8vw;
					margin-right: 8vw;
				}
			}
			.content-wrap{
				h3{
					background-image: url("~/assets/img/activities-icon-left.svg");
					background-position: left 90%;
					background-repeat: no-repeat;
					background-size: 3vw;
					text-align: right;
					span.title{
						margin-left: auto;
						margin-right: -10vw;
					}
				}
			}
		}

		&.times{
			.eyecatch-wrap{
				background-color: rgba($times-color, 0.7);
			}
			.eyecatch, .link a{
				background-color: $times-color !important;
			}
		}

		&.meets{
			.eyecatch-wrap{
				background-color: rgba($meets-color, 0.7);
			}
			.eyecatch, .link a{
				background-color: $meets-color !important;
			}
			.link a{
				color: $key-color !important;
				img {
					margin-right: 0.4em;
				}
			}
		}
	}

	> *{
		z-index: 3;
		position: relative;
	}
	.clip-polygon{
		z-index: 1;
		position: absolute;
		bottom: 0;
		width: 52vw;
		height: 52vw;
		clip-path: polygon(0 0, 0 100%, 100% 100%);
		background-color: #FFFFFF;
	}
}
</style>
