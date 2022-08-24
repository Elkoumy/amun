import React from 'react'

import PropTypes from 'prop-types'

import OutlineButton from './outline-button'

const PlaceCard = (props) => {
  return (
    <>
      <div className="place-card-container">
        <img
          alt={props.image_alt}
          src={props.image}
          className="place-card-image"
        />
        <div className="place-card-container1">
          <span className="place-card-text">{props.city}</span>
          <span className="place-card-text1">{props.description}</span>
          <OutlineButton button1="Discover place"></OutlineButton>
        </div>
      </div>
      <style jsx>
        {`
          .place-card-container {
            width: 300px;
            display: flex;
            align-items: center;
            flex-direction: column;
          }
          .place-card-image {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: var(--dl-radius-radius-radius4);
            border-top-left-radius: var(--dl-radius-radius-radius8);
            border-top-right-radius: var(--dl-radius-radius-radius8);
          }
          .place-card-container1 {
            width: 100%;
            display: flex;
            padding: var(--dl-space-space-unit);
            align-items: center;
            flex-direction: column;
          }
          .place-card-text {
            font-size: 20px;
            font-style: normal;
            font-weight: 700;
            padding-bottom: var(--dl-space-space-halfunit);
          }
          .place-card-text1 {
            font-size: 12px;
            max-width: 250px;
            margin-bottom: var(--dl-space-space-doubleunit);
          }
          @media (max-width: 767px) {
            .place-card-container {
              width: 200px;
            }
          }
          @media (max-width: 479px) {
            .place-card-container {
              width: 300px;
            }
          }
        `}
      </style>
    </>
  )
}

PlaceCard.defaultProps = {
  image:
    'https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb&w=1000',
  image_alt: 'image',
  city: 'City Name',
  description:
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.',
}

PlaceCard.propTypes = {
  image: PropTypes.string,
  image_alt: PropTypes.string,
  city: PropTypes.string,
  description: PropTypes.string,
}

export default PlaceCard
