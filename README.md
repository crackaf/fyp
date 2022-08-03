# Self Embedding Watermarking System

| Name | Rollno |
|--|--|
| Arbab Hamd Rizwan | 18L-0756 |
| Muhammad Hunzlah Malik | 18L-1139 |
| Aashar Naseem | 18L-1131 |
| Usama Aslam | 18L-0972 |

Supervisor: Dr. Asif Mahmood Gilani

> NOTE: For more details about this FYP, refer to the finalized report in "Deliverables/FYP 2/Final Evaluation" folder

## Folder Structure

```py
Self Embedding Watermarking System
├── Code
│   ├── backend
│   ├── frontend
│   ├── modules
│   │   ├── triple-recovery # Paper implementation for Image
│   │   └── video-recovery # Extending triple recovery to Video
│   └── raw # raw code files
├── Conference Paper
├── Deliverables
│   ├── FYP 1
│   │   ├── Deliverable 1 (Proposal)
│   │   ├── Deliverable 2
│   │   ├── Deliverable 3
│   │   ├── Deliverable 4
│   │   ├── FYP Registration
│   │   ├── Final Evaluation
│   │   └── Mid Evaluation
│   └── FYP 2
│       ├── Deliverable 1
│       ├── Deliverable 2
│       ├── Deliverable 3
│       ├── Deliverable 4
│       ├── Final Evaluation
│       ├── Mid Evaluation
│       └── Poster
├── Reference Material
│   ├── Image
│   ├── Keyframe Extraction
│   └── Video
└── structure.txt # Structure of all the files
```

## Abstract

These days, media editing software is very easily accessible on the internet, which leads to the issue of manipulating and tampering with either an image or a video. To address this issue, we created a system that is a web application that digitally watermarks media and then allows users to detect tampering and restore the media to its original state. In the case of an image, our system watermarks it by inserting both the authentication and restoration bits into the LSB of the image's sub blocks, which are used to detect image tampering and restoration. Similarly, in the case of video, our system first selects key frames from the stream of frames and watermarks it by inserting both the authentication and restoration bits into the LSB of the video's extracted frame/s sub blocks. To determine whether or not the media has been tampered with, compute the hash value of the watermarked media and compare it to the authentication bits, which is actually the hash value computed from the original image. If the hash values are the same, the image has not been tampered with; otherwise, it has been tampered with. Similarly, the original media content is restored using data extracted from restoration bits. The experimental results shows that the image can be restored up to 75%, implying that even if 75% of the image has been altered, it can be restored to its original state. However, in the case of video, the restoration percentage is 67 percent, implying that it can withstand attacks of up to 67 percent. The system's main functionalities include the ability to watermark media, detect tampering, and finally restore media. Furthermore, the system enables users to upload and download content from the web application. The entire processing is done on the server side in our system, so the user only needs to upload the content and download either watermarked or restored content. Our system requires a lot of computation powers which can be a limit for a single server. To deal with this issue we are also shifting to serverless programming to achieve concurrency in video watermark embedding, authentication and recovery. 


> Note: 
> Copy is available online. 
>
> [Google Drive](https://drive.google.com/drive/folders/16DEt-OtEIb3ZyUdSrkT5bF9QngHf9S7v?usp=sharing)
>
> [GitHub](https://github.com/crackaf/fyp)

