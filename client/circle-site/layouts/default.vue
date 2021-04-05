<template>
	<div>
		<header>
			<nav>
				<ul>
					<li>
						<nuxt-link to="/">top</nuxt-link>
					</li>
					<!--<li>
						<nuxt-link to="news">news</nuxt-link>
					</li>-->
					<!--<li>
						<nuxt-link to="works">works</nuxt-link>
					</li>-->
					<li>
						<!--<nuxt-link to="entry">entry</nuxt-link>-->
						<a href="https://forms.gle/DnCk411WJ8YCt8ABA">entry</a>
					</li>
					<li class="contact-link">
						<!--<nuxt-link to="contact"><img src="~/assets/img/mail.svg" alt="mail"></nuxt-link>-->
						<a href="mailto:info@iniad-wm.com"><img src="~/assets/img/mail.svg" alt="mail"></a>
					</li>
				</ul>
			</nav>
		</header>
		<main>
			<Nuxt/>
		</main>
		<footer>
			<p><a href="https://twitter.com/iniad_webmedia"><img src="~/assets/img/twitter.svg" alt="Twitter"></a></p>
			<p><small>&copy; 2021 Webメディア研究会</small></p>
		</footer>
	</div>
</template>

<style lang="scss">
header {
	background-color: $key-color;
	border-bottom: #707070 1px solid;
	letter-spacing: 3px;
	nav{
		width: 100%;
		ul{
			padding: 0;
			width: 100%;
			display: flex;
			justify-content: flex-end;
			align-items: center;
			li{
				padding: 1.25vw 2.5vw;
				font-size: 1.25vw;
				&.contact-link{
					background-color: $circle-color;
					padding: 1.25vw;
					margin-left: 1.25vw;
					display: flex;
					justify-content: center;
					align-items: center;
					img{
						display: block;
						height: 2vw;
					}
				}

				a{
					color: #FFFFFF;
				}
			}
		}
	}
}

footer {
	background-color: $key-color;
	color: #FFFFFF;
	text-align: center;
	overflow: hidden;
	p{
		margin: 1.5em 0;
		img{
			width: 3em;
		}
	}
}
</style>
