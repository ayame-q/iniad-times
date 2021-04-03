<template>
	<section class="promotion-video">
		<iframe src="https://www.youtube.com/embed/NJ54NGLteVo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
	</section>
</template>

<script>
export default {
}
</script>

<style lang="scss">
.promotion-video {
	background-color: $key-color;
	display: flex;
	justify-content: center;
	margin: 10% 0;
	margin-bottom: 0;
	iframe{
		width: 55vw;
		height: calc(55vw / 16 * 9);
	}
}
</style>
