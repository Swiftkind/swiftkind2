$(document).ready(function() {
    //triggers navbar's menu to open or close

    var cameraPositionZ = 9000;
    $('.loading').addClass('site-loading');

    setTimeout(function() {
        cameraPositionZ = 30000;
        //hides the loading screen
        $('.loading').removeClass('site-loading');

        //displays the contents of the body after the loading screen
        $('body').addClass('site-loaded');

        //triggers the menu bar animation
        $('.menu-toggle').on('click', function() {
            $('body').toggleClass('menu-open');
        });

        // initialize swiper rtl
        var swiper = new Swiper('.swiper__generic', {


            pagination: {
                el: '.swiper-pagination',
                type: 'fraction',
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                1024: {
                    slidesPerView: 1,
                    spaceBetween: 55,
                },
                768: {
                    slidesPerView: 1,
                    spaceBetween: 0,
                },
                320: {
                    slidesPerView: 2,
                    spaceBetween: 0,
                    centeredSlides: true,
                }
            }
        });

        //testimony slider

        var swiper = new Swiper('.testimony--swiper', {
            pagination: {
                el: '.swiper-pagination'
            },
        });


        //project before redirect animation
        $('.projects--item  .more-details').on('click', function(e) {
            $(".projects--item .projects--img").toggleClass('heartBeat');
            $(".projects--item").toggleClass('redirecting');
            e.preventDefault(); //will stop the link href to call the blog page
            console.log('working');
            // setTimeout(function() {
            //     window.location.href = "index.html";
            // }, 1000);
        });


        //initialize wow js

        wow = new WOW({
            boxClass: 'wow', // default
            animateClass: 'animated', // default
            offset: 0, // default
            mobile: true,
            live: true // default
        })
        wow.init();

        //initialize stickybits

        // $('.sticky').stickybits({
        //     useStickyClasses: true,
        //     stickyBitStickyOffset: 300
        // });


        //initialize rellax js

        var rellax = new Rellax('.rellax');

        (function() {

            var c = document.getElementById('bubbles'),
                randomN = function(start, end) {
                    return Math.random() * end + start;
                },
                i = 0,
                generateBubble = function() {
                    if (i < 60) {
                        var el = document.createElement('div'),
                            size = randomN(2, 7);
                        el.setAttribute('style', 'width: ' + size + 'px; height: ' + size + 'px; left:' + randomN(1, c.offsetWidth - (size + 4)) + 'px;');
                        c.appendChild(el);
                        i++;
                    } else {
                        clearInterval(inter);
                    }
                };

            generateBubble();

            var inter = setInterval(generateBubble, 200);

        })();


    }, 2000);


    var screen = $(window).width();

    //calls drawdots whenever screen is not ipad/tablet
    var is_iPad = navigator.userAgent.match(/iPad/i) != null;
    if (is_iPad == false) {
        drawDots();
    }

    //draws particles on html
    function drawDots() {
        if (WEBGL.isWebGLAvailable() === false) {
            document.body.appendChild(WEBGL.getWebGLErrorMessage());
        }
        var container;
        var camera, scene, renderer;
        var spheres = [];
        var mouseX = 0;
        var mouseY = 0;
        var windowHalfX = window.innerWidth / 2;
        var windowHalfY = window.innerHeight / 2;
        document.addEventListener('mousemove', onDocumentMouseMove, false);
        init();
        animate();

        function init() {
            container = document.createElement('div');
            document.body.appendChild(container);
            camera = new THREE.PerspectiveCamera(20, window.innerWidth / window.innerHeight, 1, 100000);
            camera.position.z = 9000;
            scene = new THREE.Scene();
            scene.background = new THREE.Color().setHSL(1, 1, 1);
            var geometry = new THREE.SphereBufferGeometry(10, 2, 16);
            var material = new THREE.MeshBasicMaterial({ color: '#d8dde5' });
            for (var i = 0; i < 200; i++) {
                var mesh = new THREE.Mesh(geometry, material);
                mesh.position.x = Math.random() * 10000 - 5000;
                mesh.position.y = Math.random() * 10000 - 5000;
                mesh.position.z = Math.random() * 10000 - 5000;
                mesh.scale.x = mesh.scale.y = mesh.scale.z = Math.random() * 3 + 1;
                scene.add(mesh);
                spheres.push(mesh);
            }
            //
            renderer = new THREE.WebGLRenderer();
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
            container.appendChild(renderer.domElement);
            //
            window.addEventListener('resize', onWindowResize, false);
        }

        function onWindowResize() {
            windowHalfX = window.innerWidth / 2;
            windowHalfY = window.innerHeight / 2;
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function onDocumentMouseMove(event) {
            mouseX = (event.clientX - windowHalfX) * 100;
            mouseY = (event.clientY - windowHalfY) * 100;
        }
        //
        function animate() {
            requestAnimationFrame(animate);
            render();
        }

        function render() {
            var timer = 0.00002 * Date.now();
            for (var i = 0, il = spheres.length; i < il; i++) {
                var sphere = spheres[i];
                sphere.position.x = 5000 * Math.cos(timer + i);
                sphere.position.y = 5000 * Math.sin(timer + i * 1.1);
            }
            camera.position.x += (mouseX - camera.position.x) * .05;
            camera.position.y += (-mouseY - camera.position.y) * .05;
            camera.lookAt(scene.position);
            renderer.render(scene, camera);
        }
    }

});