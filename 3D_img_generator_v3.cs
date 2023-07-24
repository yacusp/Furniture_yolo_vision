using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ImageGenerator : MonoBehaviour
{
    public string OUTPUT_DIRECTORY = "OUTPUTFOLDER";    
    public int IMAGE_NUM = 0;
	public float MIN_SCALE = 2.7f;
    public float MAX_SCALE = 5.0f;

    Camera myCamera;
    Light lightComp;
    GameObject light;
    int resWidth = 1600;
    int resHeight = 1200;
    int count = 0;

    // Start is called
    void Start()
    {
        myCamera = GameObject.Find("Main Camera").GetComponent<Camera>();
        
        light = new GameObject("Light");
        lightComp = light.AddComponent<Light>();

    }

    // Update is called once per frame
    void Update()
    {
        if (IMAGE_NUM > count)
        {
            float cintensity = Random.Range(0.5f, 1.0f);

            lightComp.transform.position = new Vector3(Random.Range(-100, 100), Random.Range(-100, 100), Random.Range(-100, 100));
            lightComp.color = new Vector4(cintensity, cintensity, cintensity, 1.0f);
            lightComp.intensity = Random.Range(0.5f, 1.3f);
            lightComp.type = LightType.Directional;

            float scale = Random.Range(MIN_SCALE, MAX_SCALE);

            transform.position = new Vector3(Random.Range(-60.0f, 60.0f), Random.Range(-50.0f, 50.0f), 100);
            transform.localScale = new Vector3(scale, scale, scale);
            transform.localRotation = Quaternion.Euler(Random.Range(-18.0f, 18.0f), Random.Range(-180.0f, 180.0f), Random.Range(-18.0f, 18.0f));
        }

    }

    void LateUpdate()
    {
        if (IMAGE_NUM > count)
        {
            RenderTexture rt = new RenderTexture(resWidth, resHeight, 24);
            myCamera.targetTexture = rt;
            Texture2D screenShot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
            myCamera.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
            myCamera.targetTexture = null;
            RenderTexture.active = null; 
            Destroy(rt);
            byte[] bytes = screenShot.EncodeToPNG();
            count++;
            System.IO.File.WriteAllBytes(OUTPUT_DIRECTORY + (count).ToString() + ".png", bytes);
        }
    }

}


