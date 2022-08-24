import React from 'react'

import PropTypes from 'prop-types'

const OutlineButton = (props) => {
  return (
    <>
      <div className="outline-button-container">
        <button className="outline-button-button button">
          {props.button1}
        </button>
      </div>
      <style jsx>
        {`
          .outline-button-container {
            display: flex;
            position: relative;
          }
          .outline-button-button {
            color: var(--dl-color-gray-black);
            padding-top: var(--dl-space-space-unit);
            border-color: var(--dl-color-primary-100);
            border-width: 1px;
            padding-left: var(--dl-space-space-doubleunit);
            border-radius: 50px;
            padding-right: var(--dl-space-space-doubleunit);
            padding-bottom: var(--dl-space-space-unit);
            background-color: var(--dl-color-gray-white);
          }
        `}
      </style>
    </>
  )
}

OutlineButton.defaultProps = {
  button1: 'Button',
}

OutlineButton.propTypes = {
  button1: PropTypes.string,
}

export default OutlineButton
