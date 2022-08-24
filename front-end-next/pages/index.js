import React from 'react'
import Link from 'next/link'
import Head from 'next/head'

import Component5 from '../components/component5'
import SolidButton from '../components/solid-button'
import Component4 from '../components/component4'
import FeatureCard from '../components/feature-card'
import FeatureCard1 from '../components/feature-card1'
import FeatureCard2 from '../components/feature-card2'
import FeatureCard5 from '../components/feature-card5'

const Home = (props) => {
  return (
    <>
      <div className="home-container">
        <Head>
          <title>Amun</title>
          <meta property="og:title" content="Amun" />
        </Head>
        <div className="home-top-container">
          <nav data-role="Header" className="home-navbar">
            <h1>Amun</h1>
            <div className="home-right-side">
              <div className="home-links-container">
                <span className="home-text">Home</span>
                <Link href="/about">
                  <a className="home-link">About</a>
                </Link>
                <Link href="/contact">
                  <a className="home-link1">Contact</a>
                </Link>
              </div>
              <div className="home-container1">
                <Link href="/upload">
                  <a className="home-link2">
                    <Component5 className="home-component"></Component5>
                  </a>
                </Link>
              </div>
            </div>
            <div data-type="BurgerMenu" className="home-burger-menu">
              <svg viewBox="0 0 1024 1024" className="home-burger-menu">
                <path d="M810.667 725.333h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
                <path d="M810.667 426.667h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
                <path d="M810.667 128h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
              </svg>
            </div>
            <div data-type="MobileMenu" className="home-mobile-menu">
              <div className="home-nav">
                <div className="home-top">
                  <h1>Travel</h1>
                  <div data-type="CloseMobileMenu" className="home-close-menu">
                    <svg viewBox="0 0 1024 1024" className="home-icon03">
                      <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                    </svg>
                  </div>
                </div>
                <div className="home-right-side1">
                  <div className="home-links-container1">
                    <span className="home-text01">Home</span>
                    <span className="home-text02">About</span>
                    <span className="home-text03">Tour Packages</span>
                    <span>Contact</span>
                  </div>
                  <SolidButton button="Explore places"></SolidButton>
                </div>
              </div>
              <div className="home-follow-container">
                <span className="home-text05">
                  Follow us on
                  <span
                    dangerouslySetInnerHTML={{
                      __html: ' ',
                    }}
                  />
                </span>
                <div className="home-icons-container">
                  <a
                    href="https://instagram.com"
                    target="_blank"
                    rel="noreferrer noopener"
                    className="home-link3"
                  >
                    <svg
                      viewBox="0 0 877.7142857142857 1024"
                      className="home-icon05"
                    >
                      <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
                    </svg>
                  </a>
                  <a
                    href="https://facebook.com"
                    target="_blank"
                    rel="noreferrer noopener"
                    className="home-link4"
                  >
                    <svg
                      viewBox="0 0 602.2582857142856 1024"
                      className="home-icon07"
                    >
                      <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
                    </svg>
                  </a>
                  <a
                    href="https://twitter.com"
                    target="_blank"
                    rel="noreferrer noopener"
                    className="home-link5"
                  >
                    <svg
                      viewBox="0 0 950.8571428571428 1024"
                      className="home-icon09"
                    >
                      <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </nav>
          <div className="home-hero">
            <div className="home-content-container">
              <h1 className="heading home-text06">Amun</h1>
              <h2 className="subheading home-subheading">
                Anonymize your event log.
              </h2>
              <span className="home-text07">
                <span>
                  <span
                    dangerouslySetInnerHTML={{
                      __html: ' ',
                    }}
                  />
                </span>
                <br></br>
              </span>
              <div className="home-container2">
                <Link href="/upload">
                  <a className="home-link6">
                    <Component4 className="home-component2"></Component4>
                  </a>
                </Link>
              </div>
            </div>
          </div>
        </div>
        <div className="home-features">
          <h1 className="home-text10">Amun offers the following features</h1>
          <div className="home-separator"></div>
          <div className="home-container3">
            <div className="home-container4">
              <FeatureCard text="Amun enables you to estimate the risk correlated with revealing a specific user trace and revealing each activity execution within the trace."></FeatureCard>
              <FeatureCard1 text="Amun estimates the optimal amount of noise to apply differential privacy for each user trace in your event log."></FeatureCard1>
              <FeatureCard2
                text="Amun can filter the risky user traces out of your event log."
                heading="Risky User Traces Filtration"
              ></FeatureCard2>
              <FeatureCard5
                text="Amun scales up with large-scale event logs."
                heading="Scalable Processing"
              ></FeatureCard5>
            </div>
            <img
              alt="image"
              src="https://images.unsplash.com/photo-1590613607026-15c463e30ca5?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDE0fHxzZWN1cml0eXxlbnwwfHx8fDE2NjA3NDI1MDY&amp;ixlib=rb-1.2.1&amp;w=500"
              className="home-image"
            />
          </div>
        </div>
        <footer className="home-footer">
          <span className="home-text11">
            © 2022 Gamal Elkoumy, All Rights Reserved.
          </span>
        </footer>
      </div>
      <style jsx>
        {`
          .home-container {
            width: 100%;
            height: auto;
            display: flex;
            min-height: 100vh;
            align-items: center;
            flex-direction: column;
          }
          .home-top-container {
            width: 100%;
            height: 600px;
            display: flex;
            align-items: center;
            flex-direction: column;
            background-size: cover;
            background-image: url('/playground_assets/gdpr.svg');
          }
          .home-navbar {
            width: 100%;
            display: flex;
            padding: var(--dl-space-space-doubleunit);
            max-width: 1000px;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-right-side {
            display: flex;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-links-container {
            display: flex;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-text {
            margin-right: var(--dl-space-space-doubleunit);
          }
          .home-link {
            margin-right: var(--dl-space-space-doubleunit);
            text-decoration: none;
          }
          .home-link1 {
            margin-right: var(--dl-space-space-doubleunit);
            text-decoration: none;
          }
          .home-container1 {
            border: 2px dashed rgba(120, 120, 120, 0.4);
            display: flex;
            position: relative;
          }
          .home-link2 {
            display: contents;
          }
          .home-component {
            text-decoration: none;
          }
          .home-burger-menu {
            display: none;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-burger-menu {
            width: 24px;
            height: 24px;
          }
          .home-mobile-menu {
            top: 0px;
            flex: 0 0 auto;
            left: 0px;
            width: 100%;
            height: 100%;
            display: none;
            padding: var(--dl-space-space-doubleunit);
            z-index: 100;
            position: absolute;
            flex-direction: column;
            justify-content: space-between;
            background-color: #fff;
          }
          .home-nav {
            flex: 0 0 auto;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
          }
          .home-top {
            flex: 0 0 auto;
            width: 100%;
            display: flex;
            align-items: center;
            margin-bottom: var(--dl-space-space-doubleunit);
            flex-direction: row;
            justify-content: space-between;
          }
          .home-close-menu {
            flex: 0 0 auto;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
          }
          .home-icon03 {
            width: 24px;
            height: 24px;
          }
          .home-right-side1 {
            width: 100%;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
            justify-content: space-between;
          }
          .home-links-container1 {
            display: flex;
            align-items: flex-start;
            margin-bottom: 16px;
            flex-direction: column;
            justify-content: space-between;
          }
          .home-text01 {
            margin-bottom: 8px;
          }
          .home-text02 {
            margin-bottom: 8px;
          }
          .home-text03 {
            margin-bottom: 8px;
          }
          .home-follow-container {
            display: flex;
            align-items: flex-start;
            flex-direction: column;
            justify-content: space-between;
          }
          .home-text05 {
            padding-bottom: var(--dl-space-space-halfunit);
          }
          .home-icons-container {
            width: 100px;
            display: flex;
            align-items: flex-start;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-link3 {
            display: contents;
          }
          .home-icon05 {
            width: 24px;
            height: 24px;
          }
          .home-link4 {
            display: contents;
          }
          .home-icon07 {
            width: 24px;
            height: 24px;
          }
          .home-link5 {
            display: contents;
          }
          .home-icon09 {
            width: 24px;
            height: 24px;
          }
          .home-hero {
            flex: 1;
            width: 100%;
            display: flex;
            max-width: 1000px;
            align-items: center;
            padding-top: var(--dl-space-space-tripleunit);
            padding-left: var(--dl-space-space-doubleunit);
            padding-right: var(--dl-space-space-doubleunit);
            flex-direction: row;
            padding-bottom: var(--dl-space-space-tripleunit);
            justify-content: space-between;
          }
          .home-content-container {
            display: flex;
            align-items: flex-start;
            flex-direction: column;
          }
          .home-text07 {
            padding-top: var(--dl-space-space-doubleunit);
            padding-bottom: var(--dl-space-space-doubleunit);
          }
          .home-container2 {
            border: 2px dashed rgba(120, 120, 120, 0.4);
            display: flex;
            position: relative;
          }
          .home-link6 {
            display: contents;
          }
          .home-component2 {
            text-decoration: none;
          }
          .home-features {
            width: 100%;
            display: flex;
            padding: 48px;
            max-width: 1400px;
            flex-direction: column;
          }
          .home-text10 {
            font-size: 3rem;
            margin-bottom: 32px;
          }
          .home-separator {
            width: 100px;
            height: 2px;
            background-color: var(--dl-color-gray-500);
          }
          .home-container3 {
            flex: 0 0 auto;
            width: 100%;
            display: flex;
            margin-top: 32px;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .home-container4 {
            display: grid;
            grid-template-columns: 1fr 1fr;
          }
          .home-image {
            width: 450px;
            height: 450px;
            object-fit: cover;
            flex-shrink: 0;
            margin-left: 64px;
            border-radius: var(--dl-radius-radius-round);
            object-position: left;
          }
          .home-footer {
            width: 100%;
            display: flex;
            max-width: 1400px;
            align-items: center;
            padding-top: 32px;
            padding-left: 48px;
            padding-right: 48px;
            padding-bottom: 32px;
            justify-content: space-between;
          }
          @media (max-width: 991px) {
            .home-top-container {
              background-size: cover;
              background-image: url('/playground_assets/gdpr.svg');
            }
            .home-hero {
              padding-left: var(--dl-space-space-tripleunit);
              padding-right: var(--dl-space-space-tripleunit);
            }
            .home-features {
              align-items: center;
            }
            .home-container3 {
              flex-direction: column;
            }
            .home-image {
              width: 300px;
              height: 300px;
              margin-top: 32px;
              margin-left: 0px;
            }
          }
          @media (max-width: 767px) {
            .home-right-side {
              display: none;
            }
            .home-burger-menu {
              display: flex;
            }
            .home-hero {
              justify-content: center;
            }
            .home-content-container {
              align-items: center;
            }
            .home-text06 {
              font-size: 2.5rem;
            }
            .home-text07 {
              text-align: center;
            }
            .home-features {
              padding-left: 32px;
              padding-right: 32px;
            }
            .home-text10 {
              text-align: center;
            }
            .home-container3 {
              flex-direction: column;
            }
            .home-footer {
              padding-left: 32px;
              padding-right: 32px;
            }
            .home-text11 {
              text-align: center;
              margin-left: var(--dl-space-space-unit);
              margin-right: var(--dl-space-space-unit);
            }
          }
          @media (max-width: 479px) {
            .home-text06 {
              font-size: 2rem;
              text-align: center;
            }
            .home-subheading {
              font-size: 1.3rem;
              text-align: center;
            }
            .home-features {
              padding-top: 32px;
              padding-left: var(--dl-space-space-unit);
              padding-right: var(--dl-space-space-unit);
              padding-bottom: 32px;
            }
            .home-container4 {
              grid-template-columns: 1fr;
            }
            .home-image {
              width: 250px;
              height: 250px;
            }
            .home-footer {
              padding: var(--dl-space-space-unit);
              flex-direction: column;
            }
            .home-text11 {
              margin-left: 0px;
              margin-right: 0px;
              margin-bottom: var(--dl-space-space-unit);
            }
          }
        `}
      </style>
    </>
  )
}

export default Home
