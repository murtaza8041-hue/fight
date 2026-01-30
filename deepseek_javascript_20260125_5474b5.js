// Game Variables
let gameActive = false;
let gamePaused = false;
let gameTimer = 60;
let timerInterval;
let currentRound = 1;
let maxRounds = 3;
let playerWins = 0;
let botWins = 0;
let playerCombo = 0;
let botCombo = 0;
let difficulty = 'medium';

// Player Stats
const player = {
    health: 100,
    maxHealth: 100,
    stamina: 100,
    maxStamina: 100,
    position: 150,
    isBlocking: false,
    isJumping: false,
    attackCooldown: 0
};

const bot = {
    health: 100,
    maxHealth: 100,
    stamina: 100,
    maxStamina: 100,
    position: 750,
    isBlocking: false,
    isJumping: false,
    attackCooldown: 0,
    moveDirection: 0
};

// DOM Elements
const player1Element = document.getElementById('player1');
const botElement = document.getElementById('bot');
const playerHealth = document.getElementById('playerHealth');
const playerStamina = document.getElementById('playerStamina');
const botHealth = document.getElementById('botHealth');
const botStamina = document.getElementById('botStamina');
const playerWinsElement = document.getElementById('playerWins');
const botWinsElement = document.getElementById('botWins');
const currentRoundElement = document.getElementById('currentRound');
const gameTimerElement = document.getElementById('gameTimer');
const playerComboElement = document.getElementById('playerCombo');
const botComboElement = document.getElementById('botCombo');
const roundInfoElement = document.getElementById('roundInfo');
const fightTextElement = document.getElementById('fightText');
const hitEffectElement = document.getElementById('hitEffect');
const historyLogElement = document.getElementById('historyLog');
const gameOverModal = document.getElementById('gameOverModal');
const winnerTextElement = document.getElementById('winnerText');
const modalWinnerElement = document.getElementById('modalWinner');
const modalRoundsElement = document.getElementById('modalRounds');
const modalTimeElement = document.getElementById('modalTime');

// Initialize Game
function initGame() {
    // Set initial positions
    updatePositions();
    
    // Update UI
    updateHealthBars();
    updateStaminaBars();
    updateScores();
    updateRoundInfo();
    
    // Add event listeners for buttons
    setupEventListeners();
    
    // Add keyboard controls
    setupKeyboardControls();
}

// Setup Event Listeners
function setupEventListeners() {
    // Start button
    document.getElementById('startBtn').addEventListener('click', startGame);
    
    // Restart button
    document.getElementById('restartBtn').addEventListener('click', restartGame);
    
    // Pause button
    document.getElementById('pauseBtn').addEventListener('click', togglePause);
    
    // Play again button
    document.getElementById('playAgainBtn').addEventListener('click', playAgain);
    
    // Change difficulty button
    document.getElementById('changeDifficultyBtn').addEventListener('click', () => {
        gameOverModal.style.display = 'none';
    });
    
    // Difficulty buttons
    document.querySelectorAll('.difficulty-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            document.querySelectorAll('.difficulty-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Set difficulty
            difficulty = this.getAttribute('data-difficulty');
            addLogEntry(`Difficulty changed to ${difficulty.toUpperCase()}`);
        });
    });
    
    // Control buttons (for visual feedback)
    document.querySelectorAll('.key-btn').forEach(button => {
        button.addEventListener('click', function() {
            const key = this.getAttribute('data-key');
            simulateKeyPress(key);
        });
    });
}

// Setup Keyboard Controls
function setupKeyboardControls() {
    document.addEventListener('keydown', (e) => {
        if (!gameActive || gamePaused) return;
        
        const key = e.key.toLowerCase();
        
        switch(key) {
            case 'a':
                player.position = Math.max(50, player.position - 20);
                updatePositions();
                break;
                
            case 'd':
                player.position = Math.min(850, player.position + 20);
                updatePositions();
                break;
                
            case 'w':
                if (!player.isJumping && player.stamina >= 20) {
                    player.isJumping = true;
                    player.stamina -= 20;
                    player1Element.classList.add('jump-animation');
                    setTimeout(() => {
                        player1Element.classList.remove('jump-animation');
                        player.isJumping = false;
                    }, 800);
                    addLogEntry('Player jumps!');
                }
                break;
                
            case 'j':
                if (player.attackCooldown === 0 && player.stamina >= 15) {
                    player.attackCooldown = 20;
                    player.stamina -= 15;
                    player1Element.classList.add('punch-animation');
                    setTimeout(() => {
                        player1Element.classList.remove('punch-animation');
                    }, 200);
                    
                    if (checkAttackRange()) {
                        const damage = calculateDamage('player', 'punch');
                        bot.health = Math.max(0, bot.health - damage);
                        playerCombo++;
                        botCombo = 0;
                        showHitEffect(botElement);
                        addLogEntry(`Player hits bot with punch! (-${damage} HP)`);
                        
                        if (damage > 15) {
                            addLogEntry('CRITICAL HIT!');
                        }
                    }
                }
                break;
                
            case 'k':
                if (player.attackCooldown === 0 && player.stamina >= 25) {
                    player.attackCooldown = 30;
                    player.stamina -= 25;
                    player1Element.classList.add('kick-animation');
                    setTimeout(() => {
                        player1Element.classList.remove('kick-animation');
                    }, 300);
                    
                    if (checkAttackRange()) {
                        const damage = calculateDamage('player', 'kick');
                        bot.health = Math.max(0, bot.health - damage);
                        playerCombo++;
                        botCombo = 0;
                        showHitEffect(botElement);
                        addLogEntry(`Player kicks bot! (-${damage} HP)`);
                        
                        if (damage > 20) {
                            addLogEntry('HEAVY KICK!');
                        }
                    }
                }
                break;
                
            case 'l':
                player.isBlocking = true;
                setTimeout(() => {
                    player.isBlocking = false;
                }, 500);
                break;
        }
        
        updateStaminaBars();
        updateHealthBars();
        checkRoundEnd();
    });
}

// Simulate Key Press for Button Clicks
function simulateKeyPress(key) {
    const event = new KeyboardEvent('keydown', { key: key });
    document.dispatchEvent(event);
}

// Update Positions
function updatePositions() {
    player1Element.style.left = `${player.position}px`;
    botElement.style.left = `${bot.position}px`;
}

// Update Health Bars
function updateHealthBars() {
    playerHealth.style.width = `${(player.health / player.maxHealth)