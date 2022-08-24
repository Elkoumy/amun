import React from 'react'

import PropTypes from 'prop-types'

const FeatureCard2 = (props) => {
  return (
    <>
      <div className="feature-card2-feature-card">
        <svg viewBox="0 0 1024 1024" className="feature-card2-icon">
          <path d="M809.003 291.328l-297.003 171.819-297.003-171.819 275.456-157.397c4.779-2.731 9.899-4.48 15.147-5.333 9.301-1.451 18.987 0.128 27.904 5.291zM491.776 979.669c6.016 3.243 12.928 5.077 20.224 5.077 7.381 0 14.336-1.877 20.395-5.163 15.189-2.475 29.909-7.68 43.392-15.36l298.709-170.709c26.368-15.232 45.269-38.315 55.424-64.597 5.675-14.592 8.619-30.165 8.747-46.251v-341.333c0-20.395-4.821-39.723-13.397-56.917-0.939-3.029-2.219-5.973-3.883-8.832-1.963-3.371-4.267-6.357-6.912-8.96-1.323-1.835-2.731-3.669-4.139-5.419-9.813-12.203-21.845-22.528-35.456-30.507l-299.051-170.88c-26.027-15.019-55.467-19.84-83.328-15.531-15.531 2.432-30.507 7.637-44.288 15.488l-298.709 170.709c-16.341 9.429-29.824 21.888-40.149 36.267-2.56 2.56-4.864 5.547-6.784 8.832-1.664 2.901-2.987 5.888-3.925 8.96-1.707 3.456-3.243 6.955-4.608 10.496-5.632 14.635-8.576 30.208-8.704 45.995v341.632c0.043 30.293 10.581 58.197 28.331 80.128 9.813 12.203 21.845 22.528 35.456 30.507l299.051 170.88c13.824 7.979 28.587 13.099 43.605 15.445zM469.333 537.045v340.949l-277.12-158.336c-4.736-2.773-8.832-6.315-12.16-10.411-5.931-7.381-9.387-16.512-9.387-26.581v-318.379zM554.667 877.995v-340.949l298.667-172.757v318.379c-0.043 5.163-1.067 10.496-2.987 15.445-3.413 8.789-9.6 16.384-18.176 21.333z"></path>
        </svg>
        <h2 className="feature-card2-text">{props.heading}</h2>
        <span className="feature-card2-text1">{props.text}</span>
      </div>
      <style jsx>
        {`
          .feature-card2-feature-card {
            width: 100%;
            display: flex;
            padding: var(--dl-space-space-unit);
            position: relative;
            max-width: 1400px;
            align-items: flex-start;
            flex-direction: column;
            justify-content: flex-start;
          }
          .feature-card2-icon {
            fill: var(--dl-color-gray-500);
            width: 2rem;
            height: 2rem;
            margin-bottom: var(--dl-space-space-unit);
          }
          .feature-card2-text {
            font-weight: 600;
            margin-bottom: var(--dl-space-space-unit);
          }
          .feature-card2-text1 {
            color: var(--dl-color-gray-700);
          }
          @media (max-width: 479px) {
            .feature-card2-text {
              font-style: normal;
              font-weight: 600;
            }
          }
        `}
      </style>
    </>
  )
}

FeatureCard2.defaultProps = {
  heading: 'Automatic Noise Quantification',
  text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In lorem lorem, malesuada in metus vitae, scelerisque accumsan ipsum.',
}

FeatureCard2.propTypes = {
  heading: PropTypes.string,
  text: PropTypes.string,
}

export default FeatureCard2
