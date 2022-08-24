import React from 'react'

import PropTypes from 'prop-types'

const AppComponent = (props) => {
  return (
    <>
      <div className="component-container">
        <button className="component-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .component-container {
            display: flex;
            position: relative;
          }
          .component-button {
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
          }
          .component-button:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
        `}
      </style>
    </>
  )
}

AppComponent.defaultProps = {
  button: 'Get Started',
}

AppComponent.propTypes = {
  button: PropTypes.string,
}

export default AppComponent
