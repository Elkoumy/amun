import React from 'react'

import PropTypes from 'prop-types'

const Component3 = (props) => {
  return (
    <>
      <div className="component3-container">
        <button className="component3-button button">{props.button}</button>
      </div>
      <style jsx>
        {`
          .component3-container {
            display: flex;
            position: relative;
          }
          .component3-button {
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

Component3.defaultProps = {
  button: 'Upload',
}

Component3.propTypes = {
  button: PropTypes.string,
}

export default Component3
