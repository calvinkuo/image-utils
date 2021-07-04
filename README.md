# image-utils

Image leveling utilities.

## Installation

```
pip install -r requirements.txt
```

## Usage

```
python image-utils [to_level] [to_match] [output_filename] [input_image] [output_mode]
```

Given a source image (`to_level`) and an image to match (`to_match`), it will determine the levels adjustment parameters that bring the source image closest to the image to match.
This can be useful in determining what levels adjustments were used to retouch an image with only the original image and a final resized image.

|            | Example 1                                                                                                                                                                                                                                                                          | Example 2                                                                                                                                                                                                                                                                                                                                                        |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `tolevel`  | [![A color photo](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/%E6%89%BF%E7%A5%9C%E5%A0%82%E5%85%A7%E6%99%AF.JPG/360px-%E6%89%BF%E7%A5%9C%E5%A0%82%E5%85%A7%E6%99%AF.JPG)](https://commons.wikimedia.org/wiki/File:%E6%89%BF%E7%A5%9C%E5%A0%82%E5%85%A7%E6%99%AF.JPG) | [![A black-and-white photo](https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Koninginnefeest%2C_Gasthuisstraat%2C_Inventarisnummer_NL-HlmNHA_08655.JPG/400px-Koninginnefeest%2C_Gasthuisstraat%2C_Inventarisnummer_NL-HlmNHA_08655.JPG)](https://commons.wikimedia.org/wiki/File:Koninginnefeest,_Gasthuisstraat,_Inventarisnummer_NL-HlmNHA_08655.JPG) |
| `tomatch`  | <a href="https://github.com/calvinkuo/image-utils/blob/main/examples/example1.png?raw=true"><img src="https://github.com/calvinkuo/image-utils/blob/main/examples/example1.png?raw=true"></a>                                                                                      | <a href="https://github.com/calvinkuo/image-utils/blob/main/examples/example2.png?raw=true"><img src="https://github.com/calvinkuo/image-utils/blob/main/examples/example2.png?raw=true"></a>                                                                                                                                                                    |                                                                                                                                                                                                                                                                                                                                                        |
| `output`   | <a href="https://github.com/calvinkuo/image-utils/blob/main/examples/example1output.png?raw=true"><img src="https://github.com/calvinkuo/image-utils/blob/main/examples/example1output.png?raw=true" width="360"></a>                                                              | <a href="https://github.com/calvinkuo/image-utils/blob/main/examples/example2output.png?raw=true"><img src="https://github.com/calvinkuo/image-utils/blob/main/examples/example2output.png?raw=true" width="400"></a>                                                                                                                                            |
