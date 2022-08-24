import React from 'react'

import PropTypes from 'prop-types'

const Component5 = (props) => {
  return (
    <>
      <div className="component5-container">
        <button className="component5-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .component5-container {
            display: flex;
            position: relative;
          }
          .component5-button {
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

Component5.defaultProps = {
  button: 'Upload your log',
}

Component5.propTypes = {
  button: PropTypes.string,
}

export default Component5
