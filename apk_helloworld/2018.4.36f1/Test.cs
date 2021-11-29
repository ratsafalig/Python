using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Debug.Log("hello world start");    
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log("hello world update");
        this.gameObject.transform.Rotate(new Vector3(123,456,789));    
    }
}
