<template>
	<section class="ask-or-join-wrap">
		<h2>
			<span class="title">Ask or Join</span>
			<span class="subtitle">入会のご案内</span>
		</h2>
		<div class="ask-or-join">
			<div class="content">
				<section class="join-link-wrap">
					<h3>入会フォームはこちら</h3>
					<p class="join-link">
						<nuxt-link to="/entry">入会する</nuxt-link>
					</p>
				</section>
				<section class="ask-wrap">
					<div class="ask">
						<h3>お問い合わせ</h3>
						<ul>
							<li>
								<a href="mailto:info@iniad-wm.com">
									<img src="@/assets/img/mail-blue.svg" alt="Email">
									info@iniad-wm.com
								</a>
							</li>
							<li>
								<a href="https://twitter.com/iniad_webmedia">
									<img src="@/assets/img/twitter-blue.svg" alt="Twitter">
									@iniad_webmedia
								</a>
							</li>
						</ul>
					</div>
				</section>
			</div>

			<div class="clip-polygon-top-right">
				<div class="background-color"></div>
			</div>
			<div class="clip-polygon-bottom-left"></div>
		</div>
	</section>
</template>

<script>
export default {
	name: "AskOrJoin",
};
</script>

<style lang="scss" scoped>
.ask-or-join-wrap{
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

	.ask-or-join{
		width: 100vw;
		height: calc(100vw / 1920 * 726);
		overflow: hidden;
		background-image: url("assets/img/background-ask-join.jpg");
		background-size: cover;
		position: relative;

		.content{
			display: flex;
			width: 100%;
			height: 100%;
			.join-link-wrap{
				width: 50vw;
				display: flex;
				flex-direction: column;
				justify-content: center;
				align-items: flex-end;
				h3{
					font-size: 3vw;
					font-weight: normal;
					color: #FFFFFF;
				}
				.join-link{
					margin-top: 3vw;
					margin-right: 3vw;
					a{
						display: block;
						width: fit-content;
						background: #FFFFFF;
						color: $circle-color;
						font-size: 1.5vw;
						padding: 0.5em 2em;
						border-radius: 0.8vw;
					}
				}
			}

			.ask-wrap{
				width: 50vw;
				display: flex;
				justify-content: center;
				align-items: flex-start;
				.ask{
					width: 55%;
					position: relative;
					z-index: 5;
					background-color: #FFFFFF;
					padding: 3em 2em;
					font-size: 1.5vw;
					line-height: 2.5;
					border-radius: 3vw;
					box-shadow: 1.5em 1.5em rgba($key-color, 0.3);
					h3{
						color: $circle-color;
						text-align: center;
						font-size: 2.2vw;
						font-weight: normal;
						margin-bottom: 0.8em;
					}
					ul{
						list-style: none;
						padding: 0;
						li{
							a{
								color: $circle-color;
								display: flex;
								align-items: center;
								img{
									height: 3.5em;
								}
							}
						}
					}
				}
			}
		}

		.clip-polygon-top-right{
			z-index: 1;
			position: absolute;
			overflow: hidden;
			top: 0;
			right: 0;
			width: calc(100vw / 1920 * 726 * 1.29);
			height: calc(100vw / 1920 * 726);
			clip-path: polygon(0 0, 100% 0, 100% 100%);
			background-color: #FFFFFF;
			.background-color{
				background-color: rgba($circle-color, 0.1);
				width: 100%;
				height: 100%;
			}
		}
		.clip-polygon-bottom-left{
			z-index: 1;
			position: absolute;
			overflow: hidden;
			bottom: 0;
			width: calc(100vw / 1920 * 726 / 2 * 1.29);
			height: calc(100vw / 1920 * 726 / 2);
			clip-path: polygon(0 0, 0 100%, 100% 100%);
			background-color: rgba(#FFFFFF, 0.24);
		}
	}

}
</style>
