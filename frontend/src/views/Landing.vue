<template>
  <div class="landing-page">
    <!-- Header -->
    <header class="header">
      <div class="container">
        <div class="nav-wrapper">
          <div class="logo">
            <h1 class="logo-text font-display">RareVault.</h1>
          </div>
          <nav class="nav-links">
            <router-link to="/login" class="nav-link">Log In</router-link>
            <router-link to="/register" class="btn btn-primary">Sign Up</router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title font-display">
              Got vintage treasures, antiques, or rare collectibles collecting dust?
            </h1>
            <p class="hero-subtitle">
              Find fellow collectors and enthusiasts who value what you have.
            </p>
            <div class="hero-buttons">
              <router-link to="/register?role=admin" class="btn btn-primary btn-large">
                as admin
              </router-link>
              <router-link to="/register?role=user" class="btn btn-dark btn-large">
                seller / buyer
              </router-link>
            </div>
          </div>
          
          <!-- Vintage Item Visual -->
          <div class="hero-visual">
            <div class="vintage-item">
              <div class="vintage-card">
                <div class="card-content">
                  <div class="vintage-icon">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L15.09 8.26L22 9L17 14L18.18 21L12 17.77L5.82 21L7 14L2 9L8.91 8.26L12 2Z" fill="#8b5a3c"/>
                    </svg>
                  </div>
                  <h3 class="vintage-title">Rare Collectibles</h3>
                  <p class="vintage-desc">Discover unique vintage treasures</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <div class="container">
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Trusted Collectors</h3>
            <p>Connect with verified collectors and antique enthusiasts</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 16V8C20.9996 7.64928 20.9071 7.30481 20.7315 7.00116C20.556 6.69751 20.3037 6.44536 20 6.27L13 2.27C12.696 2.09446 12.3511 2.00205 12 2.00205C11.6489 2.00205 11.304 2.09446 11 2.27L4 6.27C3.69626 6.44536 3.44398 6.69751 3.26846 7.00116C3.09294 7.30481 3.00036 7.64928 3 8V16C3.00036 16.3507 3.09294 16.6952 3.26846 16.9988C3.44398 17.3025 3.69626 17.5546 4 17.73L11 21.73C11.304 21.9055 11.6489 21.9979 12 21.9979C12.3511 21.9979 12.696 21.9055 13 21.73L20 17.73C20.3037 17.5546 20.556 17.3025 20.7315 16.9988C20.9071 16.6952 20.9996 16.3507 21 16Z" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M7.5 4.21L12 6.81L16.5 4.21" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M7.5 19.79V14.6L3 12" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M21 12L16.5 14.6V19.79" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 22.81V17.81" stroke="#8b5a3c" stroke-width="2"/>
                <path d="M12 6.81L21 12L12 17.81L3 12L12 6.81" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Secure Trading</h3>
            <p>Safe and secure platform for buying and selling antiques</p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 11H15M9 15H15M17 21L20 18V7C20 5.89543 19.1046 5 18 5H6C4.89543 5 4 5.89543 4 7V18L7 21H17Z" stroke="#8b5a3c" stroke-width="2"/>
              </svg>
            </div>
            <h3>Expert Authentication</h3>
            <p>Get your items authenticated by certified experts</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Landing',
  mounted() {
    // Add any animations or effects here
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.header {
  background: white;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  background: var(--gradient-vintage);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: var(--text-primary);
}

.hero {
  padding: 4rem 0 6rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 60vh;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 600;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
  min-height: 3.5rem;
  font-weight: 600;
}

.hero-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.vintage-item {
  position: relative;
  transform: perspective(1000px) rotateY(-15deg) rotateX(10deg);
  animation: float 6s ease-in-out infinite;
}

.vintage-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 
    0 10px 25px rgba(0, 0, 0, 0.1),
    0 20px 40px rgba(0, 0, 0, 0.05),
    0 0 0 1px rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(139, 90, 60, 0.1);
  min-width: 280px;
  text-align: center;
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.vintage-icon {
  background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
  padding: 1.5rem;
  border-radius: 50%;
  border: 2px solid rgba(139, 90, 60, 0.1);
}

.vintage-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.vintage-desc {
  color: var(--text-secondary);
  margin: 0;
}

.features {
  padding: 4rem 0;
  background: white;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  text-align: center;
  padding: 2rem;
  border-radius: 1rem;
  background: var(--background-light);
  border: 1px solid var(--border-light);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.feature-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.feature-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

@keyframes float {
  0%, 100% {
    transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(0px);
  }
  50% {
    transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(-10px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .nav-wrapper {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .nav-links {
    flex-direction: column;
    width: 100%;
  }
  
  .nav-link, .btn {
    width: 100%;
    text-align: center;
  }
  
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }
  
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .btn-large {
    flex: 1;
    min-width: 200px;
  }
  
  .vintage-item {
    transform: none;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-buttons {
    flex-direction: column;
  }
  
  .btn-large {
    width: 100%;
  }
}
</style>
