<template>
    <div class="head">
        <h1>오늘 하루는 어떤 하루였나요?</h1>
    </div>
    <div class="MovieList" v-if="store.MindMoveList">
        <MindMoviePoster v-for="movie in store.MindMoveList" :key="movie.id" :movie="movie" class="movie-poster"/>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { onMounted, ref } from 'vue';
import MindMoviePoster from './MindMoviePoster.vue';

const store = useMovieStore()


onMounted( async () => {
    await store.getMind('Base')
})

</script>

<style lang="scss" scoped>
.head {
    
}
.MovieList {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    margin: 0; 
}
.movie-poster {
    width: calc((100% - 4em) / 5); 
}
.check {
    width: 300px;
    text-align: center
}
$color: #6138D8;
.button {
  text-decoration: none;
  color: white;
  font-weight: 500;
  background: $color;
  padding: 1.25em 3em 1.05em 3em;
  border-radius: 3em;
  position: relative;
  z-index: 1;
  overflow: hidden;
  transition: 1.5s;
  margin: 0 0.5em;
  background-color: #333;
  border: 1px solid #61FBFF;

  &:first-of-type:not(:last-of-type) {
    border-bottom-right-radius: 0.3em;
  }

  &:last-of-type:not(:first-of-type) {
    border-bottom-left-radius: 0.3em;
  }

  &.--outline {
    color: white;
    background: transparent;
  }

  &:before,
  &:after {
    transition: 20s;
    content: '';
    position: absolute;
    top: 0;
    transition: 2s;
    right: -50%;
    left: -50%;
    height: 0;
    padding-bottom: 200%;
    border-radius: 35%;
    z-index: -1;
  }

  &:before {
    background: linear-gradient(
      25deg,
      lighten(adjust-hue($color, 10%), 5%),
      rgba(adjust-hue($color, 10%), 0)
    );
    transform: translate3d(-5%, 4.7em, 0) rotate(330deg);
  }

  &:after {
    background: linear-gradient(
      70deg,
      adjust-hue($color, 20%),
      rgba(adjust-hue($color, 10%), 0)
    );
    transform: translate3d(5%, 4.7em, 0) rotate(0deg);
  }

  &:hover,
  &:focus {

    &.--outline {
      color: white;
      box-shadow: inset 0 0 0 2px rgba($color, 0),
        0 0 40px rgba(adjust-hue($color, 10%), 0.5);
    }

    &:before,
    &:after {
      transform: translate3d(0, -1em, 0) rotate(180deg);
    }
  }
}

</style>