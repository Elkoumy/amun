import React, {useState, useEffect} from 'react'
import axios from 'axios';
import Link from 'next/link'
import Head from 'next/head'

import Component3 from '../components/component3'
import SolidButton from '../components/solid-button'
import Component7 from '../components/component7'
import Component9 from '../components/component9'
import Component8 from '../components/component8'
import LoadingSpinner from "../components/LoadingSpinner";

const Uploadlog = (props) => {



   const [file, setFile] = useState()
  const [anonymizeState,setanonymizeState]=useState(true);
   const[anonymizeAppearnce,setanonymizeAppearnce]=useState();
    const [downloadState,setdownloadState]=useState(true);
    const [downloadAppearance,setdownloadAppearance]=useState();
    const [isLoading, setIsLoading] = useState(false);


    const [errorMessage,seterrorMessage]= useState('');
    const [mode, setmode] = useState('sampling');


  function handleChange(event) {
    setFile(event.target.files[0])
  }

function onChangeValue(event) {
  setmode(event.target.value);
  }

  function handleSubmit(event) {
    //validate the uploaded file here
    const fileSize = file.size / 1024 / 1024; // in MiB
    if (fileSize > 5) {
      alert('File size exceeds 5 MiB');
      // $(file).val(''); //for clearing with Jquery
    } else {
         event.preventDefault()
    const url = '/api/uploadLog';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    formData.append('mode',mode);
    const config = {
      headers: {
        'content-type': 'multipart/form-data',
      },
    };
    axios.post(url, formData, config).then((response) => {

      // console.log(response.data);
      // print the validation here
      // if it is not valide keep setanonymizeState(true);
      if (response.data=== 'error_csv'){
        seterrorMessage("Please make sure the file is a CSV.");
        setanonymizeState(true);
        setanonymizeAppearnce('');

      }else if (response.data==='error_timestamp'){
        seterrorMessage("Incorrect Timestamp.");
      setanonymizeState(true);
      setanonymizeAppearnce('');
      }else if (response.data==='error_column'){
         seterrorMessage("Please make sure that the file has the column names: 'case:concept:name', 'concept:name', 'time:timestamp'");
      setanonymizeState(true);
      setanonymizeAppearnce('');
      }else if (response.data==='error_null'){
        seterrorMessage("Please make sure that the file does not have null values.");
      setanonymizeState(true);
      setanonymizeAppearnce('');
      }else if (response.data==='error'){
        seterrorMessage("Please make sure that the file is in a correct CSV or XES format.");
      setanonymizeState(true);
      setanonymizeAppearnce('');
      }else if (response.data==='xes_error'){
        seterrorMessage("Please make sure that the XES file is in the correct format");
      setanonymizeState(true);
      setanonymizeAppearnce('');
      }

      else{
        seterrorMessage('');
      setanonymizeState(false);
      setanonymizeAppearnce('uploadlog-button2 button');
      }


    });

    }

  }


  function anonymize(event) {

  //  call anonymization function here
    // take the file and pass it to amun
  console.log("Calling anonymize")
       event.preventDefault()
    const url = '/api/anonymize';
    const formData = new FormData();
    formData.append('file', file);
    formData.append('fileName', file.name);
    console.log(file.name);
    const config = {
      headers: {
        'content-type': 'application/json',
        'timeout': 10000
      },
    };
    setIsLoading(true);
    setanonymizeState(true);
    axios.post(url, {
  file: file,
  filename: file.name,
    mode:mode}, config).then(response =>{
    console.log(response.data);
    if (response.data==='success'){
      setIsLoading(false);
      setanonymizeState(false);
      setdownloadState(false);
      setdownloadAppearance('uploadlog-button2 button')
    }
    });

  }

   function download(event) {
  event.preventDefault();

  const filename=file.name;
  const url = '/api/output/anonymized_'+filename;
  const link=document.createElement('a');
  link.href=url;
  link.click();

  }

  function download_risk(event) {
  event.preventDefault();

  const filename=file.name;

  const org_file_name=filename.split('.')[0];

  const url = '/api/output/'+org_file_name+'_risk.csv';
  const link=document.createElement('a');
  link.href=url;
  link.click();

  }
  return (
    <>
      <div className="uploadlog-container">
        <Head>
          <title>uploadlog - Amun</title>
          <meta property="og:title" content="uploadlog - Amun" />
        </Head>
        <nav data-role="Header" className="uploadlog-navbar">
          <h1>Amun</h1>
          <div className="uploadlog-right-side">
            <div className="uploadlog-links-container">
              <Link href="/">
                <a className="uploadlog-link">Home</a>
              </Link>
              <Link href="/about.html">
                <a className="uploadlog-link1">About</a>
              </Link>
              <Link href="/contact.html">
                <a className="uploadlog-link2">Contact</a>
              </Link>
            </div>
            <div className="uploadlog-container1">
              <Link href="/upload.html">
                <a className="uploadlog-link3">
                  <Component3 className="uploadlog-component"></Component3>
                </a>
              </Link>
            </div>
          </div>
          <div data-type="BurgerMenu" className="uploadlog-burger-menu">
            <svg viewBox="0 0 1024 1024" className="uploadlog-burger-menu">
              <path d="M810.667 725.333h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
              <path d="M810.667 426.667h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
              <path d="M810.667 128h-597.333c-47.061 0-85.333 38.272-85.333 85.333s38.272 85.333 85.333 85.333h597.333c47.061 0 85.333-38.272 85.333-85.333s-38.272-85.333-85.333-85.333z"></path>
            </svg>
          </div>
          <div data-type="MobileMenu" className="uploadlog-mobile-menu">
            <div className="uploadlog-nav">
              <div className="uploadlog-top">
                <h1>Travel</h1>
                <div
                  data-type="CloseMobileMenu"
                  className="uploadlog-close-menu"
                >
                  <svg viewBox="0 0 1024 1024" className="uploadlog-icon03">
                    <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                  </svg>
                </div>
              </div>
              <div className="uploadlog-right-side1">
                <div className="uploadlog-links-container1">
                  <span className="uploadlog-text">Home</span>
                  <span className="uploadlog-text01">About</span>
                  <span className="uploadlog-text02">Tour Packages</span>
                  <span>Contact</span>
                </div>
                <SolidButton button="Explore places"></SolidButton>
              </div>
            </div>
            <div className="uploadlog-follow-container">
              <span className="uploadlog-text04">
                Follow us on
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
              <div className="uploadlog-icons-container">
                <a
                  href="https://instagram.com"
                  target="_blank"
                  rel="noreferrer noopener"
                  className="uploadlog-link4"
                >
                  <svg
                    viewBox="0 0 877.7142857142857 1024"
                    className="uploadlog-icon05"
                  >
                    <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
                  </svg>
                </a>
                <a
                  href="https://facebook.com"
                  target="_blank"
                  rel="noreferrer noopener"
                  className="uploadlog-link5"
                >
                  <svg
                    viewBox="0 0 602.2582857142856 1024"
                    className="uploadlog-icon07"
                  >
                    <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
                  </svg>
                </a>
                <a
                  href="https://twitter.com"
                  target="_blank"
                  rel="noreferrer noopener"
                  className="uploadlog-link6"
                >
                  <svg
                    viewBox="0 0 950.8571428571428 1024"
                    className="uploadlog-icon09"
                  >
                    <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </nav>
        <div className="uploadlog-hero">
          <div className="uploadlog-container2">
            <h1 className="uploadlog-text05">
              Upload your event log to be anonymized now
            </h1>
            <span className="uploadlog-text06">
              <span>
                Each user trace in the event log should contain the attributes
                &apos;case:concept:name&apos;, &apos;concept:name&apos;, and
                &apos;time:timestamp&apos;. The timestamp should be in the UTC
                format &apos;%Y-%m-%dT%H:%M:%S.%f&apos;. An example event log
                could be found
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
              <a
                href="https://github.com/Elkoumy/amun/blob/amunet/data/paper_example.csv"
                target="_blank"
                rel="noreferrer noopener"
                className="uploadlog-link7"
              >
                here
              </a>
              <span>.</span>
            </span>

            <div>
                Please choose the anonymization mode:
              </div>
            <form className="uploadlog-form">


              <div onChange={onChangeValue}>
              <div className="uploadlog-container3">
               <input type="radio" value="sampling" name="mode" checked/> Sampling
              </div>
              <div className="uploadlog-container4">
                  <input type="radio" value="filtering" name="mode" /> Filtering + Sampling
              </div>
              <div className="uploadlog-container5">
                <input type="radio" value="oversampling" name="mode" /> Oversampling
              </div>

              </div>
            </form>


            {/*<form className="uploadlog-form1">*/}
            {/*  <span className="uploadlog-text09"> </span>*/}
            {/*</form>*/}


            <form onSubmit={handleSubmit}>
            <div className="uploadlog-btn-group">
              <div className="uploadlog-container6">
                <div className="uploadlog-container7">
                   <input type="file" onChange={handleChange } accept=".csv,.xes"/>
                  <button className={"uploadlog-button2 button"}>Upload</button>
                   <div id="msg" type="text"  >{errorMessage}</div>
                </div>
              </div>

            </div>
            </form>

            <div> <br/>   </div>
            <form onSubmit={anonymize}>
               {isLoading ? <LoadingSpinner /> : <button className={anonymizeAppearnce} type='submit'  disabled={anonymizeState}>Anonymize</button>}

            </form>

            <div> <br/>   </div>

            <form onSubmit={download}>
            <div className="uploadlog-btn-group1">
              <button className={downloadAppearance} type='submit'  disabled={downloadState}>
                Download Anonymized File
              </button>
            </div>
              </form>

            <div> <br/>   </div>

            <form onSubmit={download_risk}>
            <div className="uploadlog-btn-group2">
              <button className={downloadAppearance}  type='submit'  disabled={downloadState}>
                Download Risk Analysis
              </button>
            </div>
            </form>



          </div>
          <img
            alt="image"
            src="https://images.unsplash.com/photo-1618498081964-ab0c002e0935?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDIxfHxwcml2YWN5fGVufDB8fHx8MTY2MDczNzc4Ng&amp;ixlib=rb-1.2.1&amp;h=1500"
            className="uploadlog-image"
          />
        </div>
        <footer className="uploadlog-footer">
          <span className="uploadlog-text10">
            © 2022 University of Tartu, All Rights Reserved.
          </span>
        </footer>
      </div>
      <style jsx>
        {`
          .uploadlog-container {
            width: 100%;
            display: flex;
            overflow: auto;
            min-height: 100vh;
            align-items: center;
            flex-direction: column;
          }
          .uploadlog-navbar {
            width: 100%;
            display: flex;
            padding: var(--dl-space-space-doubleunit);
            max-width: 1000px;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-right-side {
            display: flex;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-links-container {
            display: flex;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-link {
            margin-right: var(--dl-space-space-doubleunit);
            text-decoration: none;
          }
          .uploadlog-link1 {
            margin-right: var(--dl-space-space-doubleunit);
            text-decoration: none;
          }
          .uploadlog-link2 {
            margin-right: var(--dl-space-space-doubleunit);
            text-decoration: none;
          }
          .uploadlog-container1 {
            border: 2px dashed rgba(120, 120, 120, 0.4);
            display: flex;
            position: relative;
          }
          .uploadlog-link3 {
            display: contents;
          }
          .uploadlog-component {
            text-decoration: none;
          }
          .uploadlog-burger-menu {
            display: none;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-burger-menu {
            width: 24px;
            height: 24px;
          }
          .uploadlog-mobile-menu {
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
          .uploadlog-nav {
            flex: 0 0 auto;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
          }
          .uploadlog-top {
            flex: 0 0 auto;
            width: 100%;
            display: flex;
            align-items: center;
            margin-bottom: var(--dl-space-space-doubleunit);
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-close-menu {
            flex: 0 0 auto;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
          }
          .uploadlog-icon03 {
            width: 24px;
            height: 24px;
          }
          .uploadlog-right-side1 {
            width: 100%;
            display: flex;
            align-items: flex-start;
            flex-direction: column;
            justify-content: space-between;
          }
          .uploadlog-links-container1 {
            display: flex;
            align-items: flex-start;
            margin-bottom: 16px;
            flex-direction: column;
            justify-content: space-between;
          }
          .uploadlog-text {
            margin-bottom: 8px;
          }
          .uploadlog-text01 {
            margin-bottom: 8px;
          }
          .uploadlog-text02 {
            margin-bottom: 8px;
          }
          .uploadlog-follow-container {
            display: flex;
            align-items: flex-start;
            flex-direction: column;
            justify-content: space-between;
          }
          .uploadlog-text04 {
            padding-bottom: var(--dl-space-space-halfunit);
          }
          .uploadlog-icons-container {
            width: 100px;
            display: flex;
            align-items: flex-start;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-link4 {
            display: contents;
          }
          .uploadlog-icon05 {
            width: 24px;
            height: 24px;
          }
          .uploadlog-link5 {
            display: contents;
          }
          .uploadlog-icon07 {
            width: 24px;
            height: 24px;
          }
          .uploadlog-link6 {
            display: contents;
          }
          .uploadlog-icon09 {
            width: 24px;
            height: 24px;
          }
          .uploadlog-hero {
            width: 100%;
            display: flex;
            padding: 48px;
            max-width: 1400px;
            min-height: 80vh;
            align-items: center;
            flex-direction: row;
            justify-content: space-between;
          }
          .uploadlog-container2 {
            display: flex;
            margin-right: 48px;
            padding-right: 48px;
            flex-direction: column;
          }
          .uploadlog-text05 {
            font-size: 3rem;
            max-width: 450px;
          }
          .uploadlog-text06 {
            margin-top: 32px;
            margin-bottom: 32px;
          }
          .uploadlog-form {
            width: 200px;
            height: 100px;
          }
          .uploadlog-container3 {
            position: relative;
          }
          .uploadlog-container4 {
            position: relative;
          }
          .uploadlog-container5 {
            position: relative;
          }
          .uploadlog-form1 {
            width: 200px;
            height: 100px;
          }
          .uploadlog-text09 {
            margin-top: 32px;
            margin-bottom: 32px;
          }
          .uploadlog-btn-group {
            display: flex;
            align-items: center;
            flex-direction: row;
          }
          .uploadlog-container6 {
            border: 2px dashed rgba(120, 120, 120, 0.4);
            display: flex;
            position: relative;
          }
          .uploadlog-container7 {
            display: flex;
            position: relative;
            transition: 0.3s;
          }

          .uploadlog-button {
            color: #fffafa;
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
            background-color: #2e7e2e;
          }
          .uploadlog-button:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
          .uploadlog-button1 {
            color: #fffafa;
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
            background-color: #2e7e2e;
          }
          .uploadlog-button1:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
          .uploadlog-btn-group1 {
            display: flex;
            align-items: center;
            flex-direction: row;
          }
          .uploadlog-button2 {
            color: #fffafa;
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
            background-color: #2e7e2e;
          }
          .uploadlog-button2:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
          .uploadlog-btn-group2 {
            display: flex;
            align-items: center;
            flex-direction: row;
            justify-content: flex-start;
          }
          .uploadlog-button3 {
            color: #fffafa;
            width: 281px;
            transition: 0.3s;
            padding-top: var(--dl-space-space-unit);
            padding-left: 32px;
            padding-right: 32px;
            padding-bottom: var(--dl-space-space-unit);
            background-color: #2e7e2e;
          }
          .uploadlog-button3:hover {
            color: var(--dl-color-gray-white);
            background-color: var(--dl-color-gray-black);
          }
          .uploadlog-image {
            width: 400px;
            object-fit: cover;
          }
          .uploadlog-footer {
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
          @media (max-width: 1600px) {
            .uploadlog-button3 {
              width: 281px;
            }
          }
          @media (max-width: 1200px) {
            .uploadlog-container2 {
              height: 609px;
            }
            .uploadlog-link7 {
              text-decoration: underline;
            }
            .uploadlog-button1 {
              color: rgb(255, 250, 250);
              background-color: var(--dl-color-primary-500);
            }
            .uploadlog-button2 {
              color: rgb(255, 250, 250);
              background-color: var(--dl-color-primary-700);
            }
            .uploadlog-button3 {
              color: rgb(255, 250, 250);
              width: 281px;
              background-color: var(--dl-color-gray-500);
            }
          }
          @media (max-width: 991px) {
            .uploadlog-hero {
              flex-direction: column;
            }
            .uploadlog-container2 {
              align-items: center;
              margin-right: 0px;
              margin-bottom: 32px;
              padding-right: 0px;
            }
            .uploadlog-text05 {
              text-align: center;
            }
            .uploadlog-text06 {
              text-align: center;
              padding-left: 48px;
              padding-right: 48px;
            }
            .uploadlog-text09 {
              text-align: center;
              padding-left: 48px;
              padding-right: 48px;
            }
          }
          @media (max-width: 767px) {
            .uploadlog-right-side {
              display: none;
            }
            .uploadlog-burger-menu {
              display: flex;
            }
            .uploadlog-hero {
              padding-left: 32px;
              padding-right: 32px;
            }
            .uploadlog-text06 {
              padding-left: var(--dl-space-space-unit);
              padding-right: var(--dl-space-space-unit);
            }
            .uploadlog-text09 {
              padding-left: var(--dl-space-space-unit);
              padding-right: var(--dl-space-space-unit);
            }
            .uploadlog-image {
              width: 80%;
            }
            .uploadlog-footer {
              padding-left: 32px;
              padding-right: 32px;
            }
            .uploadlog-text10 {
              text-align: center;
              margin-left: var(--dl-space-space-unit);
              margin-right: var(--dl-space-space-unit);
            }
          }
          @media (max-width: 479px) {
            .uploadlog-hero {
              padding-top: 32px;
              padding-left: var(--dl-space-space-unit);
              padding-right: var(--dl-space-space-unit);
              padding-bottom: 32px;
            }
            .uploadlog-container2 {
              margin-bottom: var(--dl-space-space-unit);
            }
            .uploadlog-btn-group {
              flex-direction: column;
            }
            .uploadlog-btn-group1 {
              flex-direction: column;
            }
            .uploadlog-btn-group2 {
              flex-direction: column;
            }
            .uploadlog-footer {
              padding: var(--dl-space-space-unit);
              flex-direction: column;
            }
            .uploadlog-text10 {
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

export default Uploadlog
