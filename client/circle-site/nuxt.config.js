export default {
	// Target: https://go.nuxtjs.dev/config-target
	target: "static",

	// Global page headers: https://go.nuxtjs.dev/config-head
	head: {
		title: "Webメディア研究会",
		htmlAttrs: {
			lang: "ja",
		},
		meta: [
			{charset: "utf-8"},
			{name: "viewport", content: "width=device-width, initial-scale=1"},
			{hid: "description", name: "description", content: "INIAD公認サークル「Webメディア研究会」の公式サイトです。\n" +
					"私たちのサークルは”みんなで作る”ことが魅力のサークルです。\n" +
					"記事作成・デザイン・システム開発・動画編集等、メンバーそれぞれの得意分野を活かしながら、連携することで様々な活動を行っています。"},
			{hid: 'keywords', name: 'keywords', content: 'INIAD, 東洋大学'},

			{hid: 'og:site_name', property: 'og:site_name', content: 'サイト名'},
			{hid: 'og:type', property: 'og:type', content: 'website'},
			{hid: 'og:url', property: 'og:url', content: 'https://about.iniad-wm.com/'},
			{hid: 'og:title', property: 'og:title', content: 'Webメディア研究会'},
			{hid: 'og:description', property: 'og:description', content: 'INIAD公認サークル「Webメディア研究会」の公式サイトです。'},
			{hid: 'og:image', property: 'og:image', content: 'https://about.iniad-wm.com/eyecatch.png'},

			{hid: 'twitter:card', name: 'twitter:card', content: 'summary_large_image'},
			{hid: 'twitter:site', name: 'twitter:site', content: '@iniad_webmedia'}
		],
		link: [
			{rel: "icon", type: "image/x-icon", href: "/favicon.ico"},
		],
	},

	// Global CSS: https://go.nuxtjs.dev/config-css
	css: [
		"@/assets/scss/common.scss"
	],

	// Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
	plugins: [
	],

	// Auto import components: https://go.nuxtjs.dev/config-components
	components: true,

	// Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
	buildModules: [
		"@nuxtjs/style-resources",
		"@nuxtjs/google-fonts"
	],

	// Style Resources Import: https://github.com/nuxt-community/style-resources-module
	styleResources: {
		scss: ["@/assets/scss/*.scss"],
	},

	// Google Fonts Config: https://google-fonts.nuxtjs.org/options
	googleFonts: {
		families: {
			Quicksand: [300, 400, 500],
		}
	},

	// Modules: https://go.nuxtjs.dev/config-modules
	modules: [
		// https://go.nuxtjs.dev/axios
		"@nuxtjs/axios",
		// https://github.com/nuxt-community/google-gtag-module
		"@nuxtjs/google-gtag",
		'cookie-universal-nuxt',
	],

	// Axios module configuration: https://go.nuxtjs.dev/config-axios
	axios: {},

	// Google gtag configuration: https://github.com/nuxt-community/google-gtag-module
	"google-gtag": {
		id: "UA-163289416-2",
	},

	// Vue.js Configration
	vue: {
		config: {
			devTools: process.env.NODE_ENV === "development",
		}
	},

	// Build Configuration: https://go.nuxtjs.dev/config-build
	build: {},

};
