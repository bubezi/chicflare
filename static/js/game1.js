const scoreEl = document.querySelector('#scoreEl')
const canvas = document.querySelector('canvas')
const c = canvas.getContext('2d')


//

canvas.width = innerWidth
canvas.height = innerHeight
//
// canvas.width = 1024
// canvas.height = 576

////////////////////////////////// ||||   Classes  |||| ///////////////////////////////////////////
class Player {
    constructor() {

        this.velocity = {
            x: 0,
            y: 0
        }

        this.rotation = 0
        this.opacity = 1

        const image = new Image()
        image.src = spaceship_img
        image.onload = () => {
            const scale = .19
            this.image = image
            this.width = image.width * scale
            this.height = image.height * scale
            this.position = {
                x: canvas.width / 2 - this.width / 2,
                y: canvas.height - this.height - 20
        }
        }
    }
    draw() {
        // c.fillStyle = 'red'
        // c.fillRect(this.position.x, this.position.y, this.width, this.height)

        c.save()
        c.globalAlpha = this.opacity
        c.translate(player.position.x + player.width/2,
                    player.position.y + player.height/2)
        c.rotate(this.rotation)
        c.translate(-player.position.x + -player.width/2,
                    -player.position.y + -player.height/2)
        c.drawImage(this.image, this.position.x, this.position.y, this.width, this.height)
        c.restore()

    }
    update() {
        if (this.image) {
            this.draw()
            this.position.x += this.velocity.x
        }
    }
}

class Projectile {
    constructor({position, velocity}) {
        this.position = position
        this.velocity = velocity
        this.radius = 4
    }
    draw() {
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI*2)
        c.fillStyle = 'red'
        c.fill()
        c.closePath()
    }
    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y
    }
}

class InvaderProjectile {
    constructor({position, velocity}) {
        this.position = position
        this.velocity = velocity
        this.width = 3
        this.height = 10
    }
    draw() {
        c.fillStyle = '#BAA0DE'
        c.fillRect(this.position.x, this.position.y, this.width, this.height)
    }
    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y
    }
}

class Particle {
    constructor({position, velocity, radius, color, fades}) {
        this.position = position
        this.velocity = velocity
        this.radius = radius
        this.color = color
        this.opacity = 1
        this.fades = fades
    }
    draw() {
        c.save()
        c.globalAlpha = this.opacity
        c.beginPath()
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI*2)
        c.fillStyle = this.color
        c.fill()
        c.closePath()
        c.restore()
    }
    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y

        if (this.fades) {
            this.opacity -= .01
        }
    }
}

class DynamicScore {
    constructor({position, velocity, radius, color, value, fades}) {
        this.position = position
        this.velocity = velocity
        this.radius = radius
        this.color = color
        this.opacity = 1
        this.value = value
        this.fades = fades
    }
    draw() {
        // c.save()
        c.fillText(this.value, this.position.x, this.position.y)
        c.fillStyle = this.color
        // c.globalAlpha = this.opacity
        // c.restore()
    }
    update() {
        this.draw()
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y

        if (this.fades) {
            this.opacity -= .05
        }
    }
}

class Invader {
    constructor({position}) {

        this.velocity = {
            x: 0,
            y: 0
        }

        const image = new Image()
        image.src = invader_img
        image.onload = () => {
            const scale = 1
            this.image = image
            this.width = image.width * scale
            this.height = image.height * scale
            this.position = {
                x: position.x,
                y: position.y
        }
        }
    }
    draw() {
        // c.fillStyle = 'red'
        // c.fillRect(this.position.x, this.position.y, this.width, this.height)

        c.drawImage(this.image, this.position.x, this.position.y, this.width, this.height)
    }

    update({velocity}) {
        if (this.image) {
            this.draw()
            this.position.x += velocity.x
            this.position.y += velocity.y
        }
    }

    shoot(invaderProjectiles){
        invaderProjectiles.push(new InvaderProjectile({
            position: {
                x: this.position.x + this.width/2,
                y: this.position.y + this.height
            },
            velocity: {
                x: 0,
                y: 5
            }
        }))
    }
}

class Grid {
    constructor() {
        this.position = {
            x: 0,
            y: 0
        }
        this.velocity = {
            x: 3,
            y: 0
        }

        this.invaders = []

        const columns = Math.floor(Math.random() * 8 + 4)
        const rows = Math.floor(Math.random() * 2 + 2)
        this.width = columns * 30

        for (let x = 0; x < columns; x++) {
            for (let y = 0; y < rows; y++) {
                this.invaders.push(
                    new Invader({
                        position: {
                            x: x * 30,
                            y: y * 30
                        }
                    }
                    )
                )
            }
        }
    }
    update(){
        this.position.x += this.velocity.x
        this.position.y += this.velocity.y
        this.velocity.y = 0
        if (this.position.x + this.width >= canvas.width || this.position.x <= 0) {
            this.velocity.x = -this.velocity.x
            this.velocity.y = 30
        }
    }
}

/////////////////////////////////////|||||  Runtime CODE  |||||///////////////////////////////////////////
const player = new Player()
const projectiles = []
const grids = []
const invaderProjectiles = []
const particles = []
const dynamicScores = []



const keys = {
    a: {
        pressed: false
    },
    d: {
        pressed: false
    },
    space: {
        pressed: false
    }
}

///////// |||||| GAME VARIABLES |||||||
let frames = 0
let randomInterval = Math.floor((Math.random() * 500) + 750)
let game = {
    over: false,
    active: true
}
let score = 0

// Background Stars
for (let i = 0; i < 100; i++){
    particles.push(new Particle({
        position: {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height
        },
        velocity: {
            x: 0,
            y: 1
        },
        radius: Math.random() * 1.5,
        color: 'white',
        fades: false
    }))
}

function createParticles({object, color, fades}) {
    for (let i = 0; i < 15; i++){
        particles.push(new Particle({
            position: {
                x: object.position.x + object.width / 2,
                y: object.position.y + object.height / 2
            },
            velocity: {
                x: (Math.random() - .5) * 2,
                y: (Math.random() - .5) * 2
            },
            radius: Math.random() * 3,
            color: color || '#BAA0DE',
            fades: fades
        }))
    }
}

function createDynamicScores({object, color, value, fades}) {
    for (let i = 0; i < 10; i++){
        dynamicScores.push(new DynamicScore({
            position: {
                x: object.position.x + object.width / 2,
                y: object.position.y + object.height / 2
            },
            velocity: {
                x: (Math.random() - .5) * 2,
                y: (Math.random() - .5) * 2
            },
            radius: Math.random() * 3,
            color: color || '#BAA033',
            value: value || '10',
            fades: fades
        }))
    }
}

function animate() {
    if (!game.active) return
    requestAnimationFrame(animate)
    c.fillStyle = 'black'
    c.fillRect(0, 0, canvas.width, canvas.height)
    player.update()

    particles.forEach((particle, j) => {
        // Renewing stars background
        if (particle.position.y - particle.radius >= canvas.height) {
            particle.position.x = Math.random() * canvas.width
            particle.position.y = -particle.radius
        }

        // Removing rendered particles
        if (particle.opacity <= 0) {
            setTimeout(() => {
                particles.splice(j, 1)
            }, 0)

        } else {
            particle.update()
        }
    })


    dynamicScores.forEach((dynamicScore, index) => {
        // Removing rendered dynamic scores
        if (dynamicScore.opacity <= 0) {
            setTimeout(() => {
                dynamicScores.splice(index, 1)
            }, 0)

        } else {
            dynamicScore.update()
        }
    })



    invaderProjectiles.forEach((invaderProjectile, index) => {
        // Removing enemy projectiles from screen
        if (invaderProjectile.position.y + invaderProjectile.height >= canvas.height) {
            setTimeout(() => {
                invaderProjectiles.splice(index, 1)
            }, 0)
        } else {invaderProjectile.update()}

        // Collision detection code for enemy projectile and player
        if (invaderProjectile.position.y + invaderProjectile.height >= player.position.y
            && invaderProjectile.position.x + invaderProjectile.width >= player.position.x
            && invaderProjectile.position.x <= player.position.x + player.width){
            setTimeout(() => {
                invaderProjectiles.splice(index, 1)
                player.opacity = 0
                game.over = true
            }, 0)
            setTimeout(() => {
                game.active = false
            }, 2000)
            createParticles({
                object: player,
                color: 'white',
                fades: true
            })
            setTimeout(() => {
                gameover()
            }, 2500)
        }
    })

    projectiles.forEach((projectile, index) =>{
        // Remove projectile after exiting screen
        if (projectile.position.y + projectile.radius <= 0) {
            setTimeout(() => {
                projectiles.splice(index, 1)
            }, 0)
        }else {
            projectile.update()
        }
    })

    grids.forEach((grid, gridIndex) => {
        grid.update()
        // Spawn enemy projectiles
        if (frames % 100 === 0 && grid.invaders.length > 0){
            grid.invaders[Math.floor(Math.random() * grid.invaders.length)].shoot(invaderProjectiles)

        }

        grid.invaders.forEach((invader, i) => {
            invader.update({velocity: grid.velocity})

            // Projectile hit Enemy
            projectiles.forEach((projectile, j) => {
                // Colliding projectile with enemy
                if (projectile.position.y - projectile.radius  <= invader.position.y + invader.height
                    && projectile.position.x + projectile.radius >= invader.position.x
                    && projectile.position.x - projectile.radius <= invader.position.x + invader.width
                    && projectile.position.y + projectile.radius >= invader.position.y) {

                    setTimeout(() => {
                        const invaderFound = grid.invaders.find(invader2 => invader2 === invader)
                        const projectileFound = projectiles.find(projectile2 => projectile2 === projectile)

                        // Remove invader and projectiles
                        if  (invaderFound && projectileFound) {
                            score += 100
                            scoreEl.innerHTML = score
                            createParticles({
                                object: invader,
                                fades: true
                            })

                            createDynamicScores({
                                object: invader,
                                color: 'white',
                                fades: true
                            })

                            grid.invaders.splice(i, 1)
                            projectiles.splice(j, 1)


                            // Altering grid width after enemy is removed from grid
                            if (grid.invaders.length > 0) {
                                const firstInvader = grid.invaders[0]
                                const lastInvader = grid.invaders[grid.invaders.length - 1]
                                grid.width = lastInvader.position.x - firstInvader.position.x + lastInvader.width
                                grid.position.x = firstInvader.position.x
                            } else {
                                grids.splice(gridIndex, 1)
                            }
                        }
                    }, 0)
                }
            })
        })
    })

    // Moving player
    const speed = 15
    const rotation_rate = .15
    if (keys.a.pressed && player.position.x >= 0) {
        player.velocity.x = -speed
        player.rotation = -rotation_rate
    }else if(keys.d.pressed && player.position.x + player.width <= canvas.width){
        player.velocity.x = speed
        player.rotation = rotation_rate
    }else{
        player.velocity.x = 0
        player.rotation = 0
    }

    // Spawning enemies
    if (frames % randomInterval === 0 ) {
        grids.push(new Grid())
        randomInterval = Math.floor((Math.random() * 1000) + 750)
    }



    frames++
}

/// AUDIO SET UP
let myAudio = document.querySelector('#audio')
myAudio.volume = 0.5
const mute = document.querySelector('#mute')
const unmute = document.querySelector('#unmute')
if (myAudio.muted){
    mute.style.display = 'none'
    unmute.style.display = 'block'
}else{
    unmute.style.display = 'none'
    mute.style.display = 'block'
}
mute.addEventListener('click', () => {
        myAudio.muted = true
        mute.style.display = 'none'
        unmute.style.display = 'block'
})
unmute.addEventListener('click', () => {
        myAudio.muted = false
        mute.style.display = 'block'
        unmute.style.display = 'none'
})




// Game functions
function gameover(){
    toggleScreen('start-screen', false)
    toggleScreen('gameover-screen', true)
    toggleScreen('game-welcome', false)
    toggleScreen('canvas', false)
    toggleScreen('gameNav', false)
    myAudio.pause()
}

function start() {
    toggleScreen('start-screen', false)
    toggleScreen('gameover-screen', false)
    toggleScreen('game-welcome', false)
    toggleScreen('canvas', true)
    toggleScreen('gameNav', true)
    myAudio.play()
    animate()
}

function toggleScreen(id, toggle) {
    let element = document.getElementById(id)
    element.style.display = (toggle) ? 'block' : 'none'
}

function startGame() {
    start()
}



// Mobile detection functions
function isMobile() {
    // return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile/i.test(navigator.userAgent)
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile/i.test(navigator.userAgent)
}

function isTouch() {
    return 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0
}

function isMobileOrTouch() {
    return isMobile() || isTouch()
}

function isMobileAndTouch() {
    return isMobile() && isTouch()
}



if(!isTouch()){
    // Desktop controls
    // Event listeners
addEventListener('keydown', ({key}) => {
    if (game.over) return
    switch (key) {
        case 'a':
            keys.a.pressed = true
            break
        case 'd':
            keys.d.pressed = true
            break
        case ' ':
            projectiles.push(new Projectile({
                position: {
                    x: player.position.x + player.width / 2,
                    y: player.position.y
                },
                velocity: {
                    x: 0,
                    y: -10
                }
    }))

            break
        case 'ArrowLeft':
            keys.a.pressed = true
            break
        case 'ArrowRight':
            keys.d.pressed = true
            break
    }
})

addEventListener('keyup', ({key}) => {
    switch (key) {
        case 'a':
            keys.a.pressed = false
            break
        case 'd':
            keys.d.pressed = false
            break
        case ' ':
            break
        case 'ArrowLeft':
            keys.a.pressed = false
            break
        case 'ArrowRight':
            keys.d.pressed = false
            break
    }
})
}else{
    // Mobile controls
    addEventListener('touchstart', ({touches}) => {
        if (game.over) return
        
        const touch = touches[0]
        const x = touch.clientX
        // const y = touch.clientY

        if (x < canvas.width / 3) {
            keys.a.pressed = true
            keys.d.pressed = false
            addEventListener('touchend', ({touches}) =>{
                keys.a.pressed = false
            })
        } else if (x > (canvas.width / 3) * 2 ) {
            keys.d.pressed = true
            keys.a.pressed = false
            addEventListener('touchend', ({touches}) =>{
                keys.d.pressed = false
            })
        } else if (x > canvas.width / 3 && x < (canvas.width / 3) * 2) {
            projectiles.push(new Projectile({
                position: {
                    x: player.position.x + player.width / 2,
                    y: player.position.y
                },
                velocity: {
                    x: 0,
                    y: -10
                }
            }))
        }

    })
}






// window.addEventListener('deviceorientation', function(event) {
//     console.log(event.absolute + ':' + event.alpha + ' : ' + event.beta + ' : ' + event.gamma);
//   });

// window.addEventListener("deviceorientation", ({event}) => {
//     console.log('event', event)
//     let absolute = event.absolute;
//     let alpha = event.alpha;
//     let beta = event.beta;
//     let gamma = event.gamma;

//     if (alpha > 2) {
//             keys.a.pressed = true
//             keys.d.pressed = false
//             console.log('left')
//         }
//     if (alpha < -2 ) {
//             keys.d.pressed = true
//             keys.a.pressed = false
//             console.log('right')
//         }

// }, true);

//
// ////////////////////// Start Page /////////////////////////////////
// let startButton = document.querySelector('#startButton')
// let selection = document.querySelector('#levels')
// let char_selection = document.querySelector('#character')
// let quantity = document.querySelector('#quantity')
//
// startButton.setAttribute("disabled","disabled")
// startButton.style.display = 'None'
//
//     selection.addEventListener("change", () => {
//     if (document.querySelector('#levels').value === "") {
//         startButton.setAttribute("disabled","disabled")
//         startButton.style.display = 'None'
//         }else{
//             char_selection.addEventListener("change", () => {
//             if(document.querySelector('#character').value === ""){
//                 }else {
//                         startButton.removeAttribute("disabled")
//                         startButton.style.display = 'inline-block'
//                 }
//             })
//     }})
//////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                  //
//                                                                                                  //
//                       Space Invaders JavaScript and HTML Canvas                                  //
//                                                                                                  //
//                                                                                                  //
//////////////////////////////////////////////////////////////////////////////////////////////////////

