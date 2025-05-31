// Material Design 动画插件
export default {
  install(app) {
    // 全局动画方法
    app.config.globalProperties.$animateIn = (element, delay = 0) => {
      if (element) {
        element.style.opacity = '0'
        element.style.transform = 'translateY(20px)'
        element.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)'
        
        setTimeout(() => {
          element.style.opacity = '1'
          element.style.transform = 'translateY(0)'
        }, delay)
      }
    }

    // 全局过渡效果
    app.config.globalProperties.$transitions = {
      page: {
        enterActiveClass: 'page-enter-active',
        leaveActiveClass: 'page-leave-active',
        enterFromClass: 'page-enter-from',
        leaveToClass: 'page-leave-to'
      },
      fade: {
        enterActiveClass: 'fade-enter-active',
        leaveActiveClass: 'fade-leave-active',
        enterFromClass: 'fade-enter-from',
        leaveToClass: 'fade-leave-to'
      },
      slide: {
        enterActiveClass: 'slide-enter-active',
        leaveActiveClass: 'slide-leave-active',
        enterFromClass: 'slide-enter-from',
        leaveToClass: 'slide-leave-to'
      }
    }

    // 全局动画样式注入
    const style = document.createElement('style')
    style.textContent = `
      /* 淡入淡出动画 */
      .fade-enter-active,
      .fade-leave-active {
        transition: opacity 0.5s ease;
      }
      .fade-enter-from,
      .fade-leave-to {
        opacity: 0;
      }

      /* 滑动动画 */
      .slide-enter-active,
      .slide-leave-active {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      }
      .slide-enter-from {
        transform: translateX(100%);
      }
      .slide-leave-to {
        transform: translateX(-100%);
      }

      /* 弹性动画 */
      .bounce-enter-active {
        animation: bounce-in 0.5s;
      }
      .bounce-leave-active {
        animation: bounce-in 0.5s reverse;
      }
      @keyframes bounce-in {
        0% {
          transform: scale(0);
        }
        50% {
          transform: scale(1.1);
        }
        100% {
          transform: scale(1);
        }
      }

      /* 涟漪效果 */
      .ripple {
        position: relative;
        overflow: hidden;
      }
      .ripple::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: all 0.6s ease;
        z-index: 1;
      }
      .ripple:hover::before {
        width: 300px;
        height: 300px;
      }

      /* 发光效果 */
      .glow {
        transition: all 0.3s ease;
      }
      .glow:hover {
        box-shadow: 0 0 20px rgba(25, 118, 210, 0.6);
      }

      /* 脉冲效果 */
      .pulse {
        animation: pulse-animation 2s infinite;
      }
      @keyframes pulse-animation {
        0% {
          box-shadow: 0 0 0 0px rgba(25, 118, 210, 0.7);
        }
        100% {
          box-shadow: 0 0 0 20px rgba(25, 118, 210, 0);
        }
      }

      /* 摇摆效果 */
      .wobble:hover {
        animation: wobble 0.8s ease-in-out;
      }
      @keyframes wobble {
        0%, 100% { transform: rotate(0deg); }
        15% { transform: rotate(-5deg); }
        30% { transform: rotate(5deg); }
        45% { transform: rotate(-5deg); }
        60% { transform: rotate(5deg); }
        75% { transform: rotate(-5deg); }
      }

      /* 弹跳效果 */
      .bounce:hover {
        animation: bounce-animation 0.6s ease;
      }
      @keyframes bounce-animation {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-15px); }
        60% { transform: translateY(-7px); }
      }

      /* 渐变文字动画 */
      .gradient-text {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-animation 4s ease infinite;
      }
      @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
      }

      /* 打字机效果 */
      .typewriter {
        overflow: hidden;
        white-space: nowrap;
        animation: typing 3s steps(40, end);
      }
      @keyframes typing {
        from { width: 0; }
        to { width: 100%; }
      }

      /* 3D 翻转效果 */
      .flip-card {
        perspective: 1000px;
      }
      .flip-card-inner {
        transition: transform 0.6s;
        transform-style: preserve-3d;
      }
      .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
      }

      /* 粒子动画背景 */
      .particles-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 198, 255, 0.3) 0%, transparent 50%);
        animation: floating 6s ease-in-out infinite;
      }
      @keyframes floating {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
      }
    `
    document.head.appendChild(style)
  }
}
