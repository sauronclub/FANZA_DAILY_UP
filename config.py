# 网址
JAPAN_IP_URL = "https://raw.githubusercontent.com/sauronclub/global-ip-ranges/refs/heads/main/random_jp_ips.json"
FANZA_VIDEO_URL = 'https://video.dmm.co.jp/av/'
FANZA_DAILY_URL = 'https://www.dmm.co.jp/digital/videoa/-/ranking/=/term=daily/'
FANZA_API_URL = 'https://api.video.dmm.co.jp/graphql'

# 最大重试次数
MAX_RETRIES = 3

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Cookie': 'age_check_done=1; ckcy=1',
#     'X-Forwarded-For': IP # 模拟来自日本的请求
# }


ID_PAYLOAD = {
    "operationName": "ContentPageData",
    "query": """query ContentPageData($id: ID!, $isLoggedIn: Boolean!, $isAmateur: Boolean!, $isAnime: Boolean!, $isAv: Boolean!, $isCinema: Boolean!, $isSP: Boolean!, $shouldFetchRelatedTags: Boolean = false, $isPhase4_2Released: Boolean!) {
  ppvContent(id: $id) {
    ...ContentData
    __typename
  }
  reviewSummary(contentId: $id) {
    ...ReviewSummary
    __typename
  }
  ...basketCountFragment
}
fragment ContentData on PPVContent {
  id
  floor
  title
  isExclusiveDelivery
  releaseStatus
  description
  notices
  isNoIndex
  isAllowForeign
  announcements {
    body
    __typename
  }
  featureArticles {
    link {
      url
      text
      __typename
    }
    __typename
  }
  packageImage {
    largeUrl
    mediumUrl
    __typename
  }
  sampleImages {
    number
    imageUrl
    largeImageUrl
    __typename
  }
  products {
    ...ProductData
    __typename
  }
  mostPopularContentImage {
    ... on ContentSampleImage {
      __typename
      largeImageUrl
      imageUrl
    }
    ... on PackageImage {
      __typename
      largeUrl
      mediumUrl
    }
    __typename
  }
  priceSummary @skip(if: $isPhase4_2Released) {
    lowestSalePrice
    lowestPrice
    campaign {
      title
      id
      endAt
      pointGrantRate
      __typename
    }
    __typename
  }
  pricing @include(if: $isPhase4_2Released) {
    lowestEffectivePriceInclusiveTax
    lowestRegularPriceInclusiveTax
    sale {
      name
      id
      endAt
      __typename
    }
    campaign {
      id
      title
      __typename
    }
    __typename
  }
  tags {
    ...TagFragment
    __typename
  }
  genres {
    ...GenreFragment
    __typename
  }
  performers {
    ...PerformerFragment
    __typename
  }
  directors {
    ...DirectorFragment
    __typename
  }
  authors {
    ...AuthorFragment
    __typename
  }
  series {
    ...SeriesFragment
    __typename
  }
  makers {
    ...MakerFragment
    __typename
  }
  labels {
    ...LabelFragment
    __typename
  }
  images {
    ...ContentImageFragment
    __typename
  }
  sampleImages {
    ...SampleImageFragment
    __typename
  }
  reviews {
    ...ReviewFragment
    __typename
  }
  relatedDeliveryContents {
    ...RelatedContentFragment
    __typename
  }
  faqs {
    ...FaqFragment
    __typename
  }
  purchasePointGrantRates {
    regular
    campaign
    __typename
  }
  purchasePointGrantRate
  __typename
}
fragment ReviewSummary on ReviewSummary {
  reviewCount
  averageRating
  __typename
}
fragment basketCountFragment on Query {
  basketCount {
    rental
    purchase
    __typename
  }
  __typename
}
fragment ProductData on Product {
  id
  productType
  salesMethod
  resolution
  duration
  isHd
  deliveryStartAt
  deliveryEndAt
  __typename
}
fragment TagFragment on Tag {
  id
  name
  __typename
}
fragment GenreFragment on Genre {
  id
  name
  __typename
}
fragment PerformerFragment on Performer {
  id
  name
  ruby
  __typename
}
fragment DirectorFragment on Director {
  id
  name
  ruby
  __typename
}
fragment AuthorFragment on Author {
  id
  name
  ruby
  __typename
}
fragment SeriesFragment on Series {
  id
  name
  ruby
  __typename
}
fragment MakerFragment on Maker {
  id
  name
  ruby
  __typename
}
fragment LabelFragment on Label {
  id
  name
  ruby
  __typename
}
fragment ContentImageFragment on ContentImage {
  imageType
  imageUrl
  __typename
}
fragment SampleImageFragment on SampleImage {
  imageUrl
  __typename
}
fragment ReviewFragment on Review {
  id
  title
  body
  rating
  helpfulCount
  unhelpfulCount
  createdAt
  user {
    name
    purchaseCount
    reviewCount
    __typename
  }
  __typename
}
fragment RelatedContentFragment on RelatedContent {
  id
  title
  imageUrl
  __typename
}
fragment FaqFragment on Faq {
  question
  answer
  __typename
}""",
    "variables": {
        "id": "placeholder_id",
        "isLoggedIn": False,
        "isAmateur": False,
        "isAnime": False,
        "isAv": True,
        "isCinema": False,
        "isSP": False,
        "shouldFetchRelatedTags": False,
        "isPhase4_2Released": False
    }
}