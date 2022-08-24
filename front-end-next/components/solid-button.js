import React from 'react'

import PropTypes from 'prop-types'

const SolidButton = (props) => {
  return (
    <>
      <div className="solid-button-container">
        <button className="solid-button-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .solid-button-container {
            display: flex;
            position: relative;
          }
          .solid-button-button {
            color: var(--dl-color-gray-white);
            border: none;
            padding-top: var(--dl-space-space-halfunit);
            padding-left: var(--dl-space-space-doubleunit);
            border-radius: 50px;
            padding-right: var(--dl-space-space-doubleunit);
            padding-bottom: var(--dl-space-space-halfunit);
            background-color: var(--dl-color-primary-100);
          }
        `}
      </style>
    </>
  )
}

SolidButton.defaultProps = {
  button: 'Button',
}

SolidButton.propTypes = {
  button: PropTypes.string,
}

export default SolidButton
