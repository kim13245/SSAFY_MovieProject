<template>
    <div v-if="visible" class="modal-backdrop" @click="close">
      <div class="modal-container" @click.stop>
        <button class="modal-close" @click="close">✖</button>
        <iframe
          v-if="videoId"
          :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
          frameborder="0"
          allow="autoplay; encrypted-media"
          allowfullscreen
          class="modal-iframe"
        ></iframe>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      visible: {
        type: Boolean,
        required: true,
      },
      videoId: {
        type: String,
        required: true,
      },
    },
    emits: ["close"],
    methods: {
      close() {
        this.$emit("close");
      },
    },
  };
  </script>
  
  <style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  .modal-container {
    position: relative;
    width: 90%;
    max-width: 800px;
    background: #000;
    padding: 0;
    border-radius: 10px;
    overflow: hidden;
  }
  .modal-close {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    color: white;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
  }
  .modal-iframe {
    width: 100%;
    height: 450px;
    border: none;
  }
  </style>