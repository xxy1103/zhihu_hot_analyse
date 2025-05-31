<template>
  <div class="floating-particles">
    <div 
      v-for="i in particleCount"
      :key="i"
      class="particle"
      :style="getParticleStyle(i)"
    ></div>
  </div>
</template>

<script>
export default {
  name: 'FloatingParticles',
  props: {
    particleCount: {
      type: Number,
      default: 20
    }
  },
  methods: {
    getParticleStyle(index) {
      const size = Math.random() * 8 + 4
      const left = Math.random() * 100
      const animationDuration = Math.random() * 10 + 5
      const animationDelay = Math.random() * 5
      
      return {
        width: `${size}px`,
        height: `${size}px`,
        left: `${left}%`,
        animationDuration: `${animationDuration}s`,
        animationDelay: `${animationDelay}s`,
        opacity: Math.random() * 0.5 + 0.3
      }
    }
  }
}
</script>

<style scoped>
.floating-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: -1;
  overflow: hidden;
}

.particle {
  position: absolute;
  background: linear-gradient(45deg, #667eea, #764ba2, #4ecdc4);
  border-radius: 50%;
  animation: float-up infinite linear;
  box-shadow: 0 0 15px rgba(102, 126, 234, 0.4),
              0 0 30px rgba(118, 75, 162, 0.2);
  backdrop-filter: blur(2px);
}

.particle::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, #667eea, #764ba2, #4ecdc4);
  border-radius: 50%;
  z-index: -1;
  filter: blur(4px);
  opacity: 0.6;
}

@keyframes float-up {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

/* 不同大小的粒子使用不同的动画 */
.particle:nth-child(odd) {
  animation-name: float-up-left;
}

.particle:nth-child(even) {
  animation-name: float-up-right;
}

@keyframes float-up-left {
  0% {
    transform: translateY(100vh) translateX(-50px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes float-up-right {
  0% {
    transform: translateY(100vh) translateX(50px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) translateX(-50px) rotate(-360deg);
    opacity: 0;
  }
}
</style>
