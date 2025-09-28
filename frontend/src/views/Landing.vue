<template>
  <div class="landing-bg">
      <div class="paper-card">
        <div class="logo-row">
          <span class="logo-text">RareVault.</span>
        </div>
        <div class="headline-row">
          <h1 class="headline">Got vintage treasures, antiques, or rare collectibles collecting dust?</h1>
        </div>
        <div class="subtitle-row">
          <div class="subtitle-band">
            <span class="subtitle">Find fellow collectors and enthusiasts who value what you have.</span>
          </div>
        </div>
        <div class="button-row">
          <router-link to="/register?role=admin" class="btn-admin">as admin</router-link>
          <router-link to="/register?role=user" class="btn-buyer">seller / buyer</router-link>
        </div>
        <div class="clip-row">
          <!-- Metallic clip SVG enlarged -->
          <svg class="clip-svg" width="220" height="140" viewBox="0 0 220 140" fill="none" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="110" cy="120" rx="90" ry="12" fill="#b08d6e" fill-opacity="0.28"/>
            <rect x="55" y="48" width="110" height="60" rx="16" fill="#b08d6e" stroke="#a07c5b" stroke-width="3"/>
            <circle cx="110" cy="78" r="18" fill="#e0c7a0" stroke="#a07c5b" stroke-width="3"/>
            <rect x="100" y="100" width="20" height="20" rx="4" fill="#a07c5b"/>
            <!-- highlight -->
            <path d="M70 58 C90 40,130 40,150 58" stroke="#ecd7bf" stroke-width="3" fill="none" opacity="0.6"/>
          </svg>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  name: 'Landing'
}
</script>

<style scoped>
.landing-bg {
  min-height: 100vh;
  width: 100vw;
  background: #000;
  display: flex;
  align-items: flex-start; /* put card toward the top so paper fills top edge */
  justify-content: center;
  overflow-x: hidden;
}

.paper-card {
  background: #fff;
  border-radius: 0 0 160px 160px/0 0 120px 120px;
  box-shadow: 0 18px 80px rgba(0,0,0,0.35), 0 1px 0 #eaeaea;
  width: 100vw; /* full width so no black on sides */
  max-width: none;
  min-height: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding: 90px 64px 160px 64px;
  margin: 0; /* remove bottom margin so edges align better */
}

.logo-row {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  margin-bottom: 32px;
}
.logo-text {
  font-family: 'Georgia', serif;
  font-size: 2rem;
  font-weight: 500;
  color: #222;
  letter-spacing: -1px;
}

.headline-row {
  width: 100%;
  text-align: center;
  margin-bottom: 18px;
}
.headline {
  font-family: 'Georgia', serif;
  font-size: 3.2rem;
  font-weight: 400;
  color: #111;
  line-height: 1.08;
  margin: 0 auto;
  max-width: 1100px;
}

.subtitle-row {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 28px;
}
.subtitle-band {
  background: #222;
  padding: 12px 48px;
  transform: rotate(-4deg);
  box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
.subtitle {
  color: #fff;
  font-size: 1.05rem;
  font-family: 'Inter', sans-serif;
  display: inline-block;
}

.button-row {
  display: flex;
  gap: 48px;
  margin-top: 18px;
  margin-bottom: 18px;
  justify-content: center;
}
.btn-admin {
  background: #2563eb;
  color: #fff;
  font-size: 1.05rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 2.2rem;
  box-shadow: 0 2px 8px rgba(37,99,235,0.08);
  cursor: pointer;
  transform: rotate(-7deg) translateY(6px);
  transition: background 0.2s, transform 0.2s;
  text-decoration: none;
}
.btn-admin:hover {
  background: #1d4ed8;
  transform: rotate(-7deg) scale(1.04);
}
.btn-buyer {
  background: #111;
  color: #fff;
  font-size: 1.05rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 2.2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  cursor: pointer;
  transform: rotate(2deg) translateY(2px);
  transition: background 0.2s, transform 0.2s;
  text-decoration: none;
}
.btn-buyer:hover {
  background: #333;
  transform: rotate(2deg) scale(1.04);
}

.clip-row {
  position: absolute;
  left: 50%;
  bottom: -68px;
  transform: translateX(-50%) rotate(-6deg);
  z-index: 3;
}
.clip-svg {
  display: block;
  filter: drop-shadow(0 12px 36px rgba(0,0,0,0.45));
}

@media (max-width: 800px) {
  .paper-card {
    width: 100vw;
    min-height: 420px;
    padding: 36px 8vw 90px 8vw;
  }
  .headline {
    font-size: 1.3rem;
    max-width: 95vw;
  }
  .logo-text {
    font-size: 1.2rem;
  }
  .btn-admin, .btn-buyer {
    font-size: 1rem;
    padding: 0.8rem 1.5rem;
  }
}

@media (max-width: 500px) {
  .paper-card {
    border-radius: 0 0 60px 60px/0 0 40px 40px;
    min-height: 320px;
    padding: 24px 2vw 70px 2vw;
  }
  .headline {
    font-size: 1rem;
    max-width: 98vw;
  }
  .logo-row {
    margin-bottom: 18px;
  }
  .subtitle-row {
    margin-bottom: 18px;
  }
  .button-row {
    gap: 12px;
    margin-top: 10px;
    margin-bottom: 10px;
  }
  .clip-row {
    bottom: -34px;
  }
  .clip-svg {
    width: 70px;
    height: 32px;
  }
}
</style>
