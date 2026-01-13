<script setup lang="ts">
import "vidstack/bundle";
import { ref, type Ref, type TrackHTMLAttributes } from "vue";

interface Props {
    player: {
        title: string
        src: string
    }
    poster: { src: string }
    textTracks: TrackHTMLAttributes[]
    layout: { thumbnails: string }
}

const props: Ref<Props> = ref({ player: { title: "", src: "" }, poster: { src: "" }, textTracks: [], layout: { thumbnails: "" } })
// const props = defineProps<Props>()

</script>

<template>
    <media-player :title="props.player.title" :src="props.player.src" cross-origin view-type="video" load="play">
        <media-provider>
            <media-poster class="vds-poster" :src="props.poster.src" />
            <track v-for="v in props.textTracks" :src="v.src" :kind="v.kind" :label="v.label" :srclang="v.srclang"
                :default="v.default" :key="v.label">
            </track>
        </media-provider>
        <media-video-layout :thumbnails="props.layout.thumbnails"></media-video-layout>
    </media-player>
</template>

<style scoped></style>